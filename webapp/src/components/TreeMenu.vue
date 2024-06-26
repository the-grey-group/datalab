<template>
  <div class="tree-menu">
    <div v-if="entry.type == 'toplevel'" class="my-2" @click="toggleChildren">
      <span :class="{ expanded: showChildren }" class="directory-arrow">&#9656;</span>
      <font-awesome-icon :icon="['fas', 'hdd']" class="toplevel-icon" />
      <span class="toplevel-name" :class="{ 'search-match': searchMatched }">
        {{ entry.name }}
      </span>
    </div>
    <div v-else-if="entry.type == 'directory'" @click="toggleChildren">
      <span :class="{ expanded: showChildren }" class="directory-arrow">&#9656;</span>
      <font-awesome-icon
        v-show="showChildren"
        :icon="['fas', 'folder-open']"
        class="directory-icon"
      />
      <font-awesome-icon v-show="!showChildren" :icon="['fas', 'folder']" class="directory-icon" />
      <span class="directory-name" :class="{ 'search-match': searchMatched }">
        {{ entry.name }}
      </span>
    </div>

    <div
      v-else-if="entry.type == 'file'"
      class="file-entry"
      :class="{ selected: isSelected }"
      @click.exact="selectFile"
      @click.meta="addFileToSelection"
      @click.ctrl="addFileToSelection"
    >
      <span class="file-icon"> &#8249; &#8250; </span>
      <span class="filename" :class="{ 'search-match': searchMatched }">
        {{ entry.name }}
      </span>
    </div>

    <div v-else-if="entry.type == 'error'" class="error-entry alert alert-danger">
      <font-awesome-icon :icon="['fas', 'exclamation-circle']" class="mr-2" />
      <span>
        {{ entry.details }}
      </span>
    </div>

    <transition
      name="collapse"
      :css="true"
      @enter="setMaxHeightToScrollHeight"
      @after-enter="removeMaxHeightStyle"
      @before-leave="setMaxHeightToScrollHeight"
      @leave="removeMaxHeightStyle"
    >
      <ol
        v-if="showChildren"
        ref="childrenBlock"
        class="child-list"
        :style="{ 'margin-left': depth * 1.5 + ' rem' }"
      >
        <li v-for="childEntry in entry.contents" :key="childEntry.name" class="child-entry">
          <!-- note: passes selection events up the tree -->
          <tree-menu
            :entry="childEntry"
            :depth="depth + 1"
            :selected-entries="selectedEntries"
            :search-term="searchTerm"
            @set-selected-entry="$emit('setSelectedEntry', $event)"
            @append-to-selected-entries="$emit('appendToSelectedEntries', $event)"
          />
        </li>
      </ol>
    </transition>
  </div>
</template>

<script>
export default {
  name: "TreeMenu",
  props: {
    entry: {
      type: Object,
      required: true,
    },
    depth: {
      type: Number,
      required: true,
    },
    selectedEntries: {
      type: Array,
      required: true,
    },
    searchTerm: {
      type: String,
      required: true,
    },
  },
  emits: ["setSelectedEntry", "appendToSelectedEntries"],
  data() {
    return {
      showChildren: false,
    };
  },
  computed: {
    isSelected() {
      return this.selectedEntries.indexOf(this.entry) != -1;
    },
    indent() {
      return { transform: `translate(${this.depth * 50}px)` };
    },
    searchMatched() {
      if (this.searchTerm.trim() == "") {
        return false;
      }
      var isMatch = this.entry.name.toLowerCase().includes(this.searchTerm.toLowerCase());
      return isMatch;
    },
  },
  methods: {
    toggleChildren() {
      this.showChildren = !this.showChildren;
    },
    selectFile() {
      console.log("emmiting setSelectedEntry up the tree");
      this.$emit("setSelectedEntry", this.entry);
      // this.isSelected = true;
    },
    addFileToSelection() {
      this.$emit("appendToSelectedEntries", this.entry);
    },
    setMaxHeightToScrollHeight(el) {
      el.style.maxHeight = el.scrollHeight + "px";
    },
    removeMaxHeightStyle(el) {
      el.style.maxHeight = null;
    },
  },
};
</script>

<style scoped>
.collapse-enter-from {
  opacity: 0;
  max-height: 0px;
}

.collapse-enter-active {
  transition: all 0.2s ease;
}

.collapse-enter-to {
  max-height: auto;
}

.collapse-leave-active {
  opacity: 0;
  max-height: 0px;
  transition: all 0.2s ease;
}

.child-list {
  list-style-type: none;
  overflow: hidden;
}

.directory-arrow {
  font-size: regular;
  color: grey;
  transition: all 0.2s;
  display: inline-block;
}

.directory-arrow.expanded {
  -webkit-transform: rotate(90deg);
  -moz-transform: rotate(90deg);
  transform: rotate(90deg);
}

.directory-icon {
  font-size: small;
  margin-left: 0.4rem;
  margin-right: 0.75rem;
  color: grey;
  transition: all 0.4s;
}

.toplevel-icon {
  font-size: medium;
  margin-left: 0.4rem;
  margin-right: 0.75rem;
  color: teal;
  transition: all 0.4s;
}

.toplevel-name {
  font-size: large;
  font-weight: 600;
  color: teal;
}

.directory-name {
  font-weight: 600;
}

.file-icon {
  margin-right: 0.5rem;
  margin-left: 0.8rem;
  color: grey;
}

.child-entry {
  padding-top: 0.1rem;
  padding-bottom: 0.1rem;
}

.file-entry {
  display: inline-block;
}

.filename {
  color: #4a4a4a;
  margin-right: 10px;
}

.error-entry {
  /*color: #b90000;*/
}

.selected {
  background: #fbeddf;
}

.search-match {
  background: #defaff;
}

.selected .filename,
.selected .file-icon {
  /*color: white;*/
  /*font-weight: 600;*/
}
</style>
