<template>
  <div id="synthesis-information">
    <label class="mr-2 pb-2">Synthesis Information</label>
    <div class="card component-card">
      <div class="card-body pt-2 pb-0 mb-0 pl-5">
        <CompactConstituentTable
          id="synthesis-table"
          v-model="constituents"
          :types-to-query="['samples', 'starting_materials']"
        />
      </div>
    </div>
    <span id="synthesis-procedure-label" class="subheading ml-2">Procedure</span>
    <TinyMceInline
      v-model="SynthesisDescription"
      aria-labelledby="synthesis-procedure-label"
    ></TinyMceInline>
  </div>
</template>

<script>
import TinyMceInline from "@/components/TinyMceInline";
import { createComputedSetterForItemField } from "@/field_utils.js";
import CompactConstituentTable from "@/components/CompactConstituentTable.vue";

export default {
  components: {
    TinyMceInline,
    CompactConstituentTable,
  },
  props: {
    item_id: { type: String, required: true },
  },
  data() {
    return {
      selectedNewConstituent: null,
      selectedChangedConstituent: null,
      selectShown: [],
    };
  },
  computed: {
    constituents: createComputedSetterForItemField("synthesis_constituents"),
    SynthesisDescription: createComputedSetterForItemField("synthesis_description"),
  },
  watch: {
    // since constituents is an object, the computed setter never fires and
    // saved status is never updated. So, use a watcher:
    constituents: {
      handler() {
        this.$store.commit("setItemSaved", { item_id: this.item_id, isSaved: false });
      },
      deep: true,
    },
  },
  mounted() {
    this.selectShown = new Array(this.constituents.length).fill(false);
  },
  methods: {
    addConstituent(selectedItem) {
      this.constituents.push({
        item: selectedItem,
        quantity: null,
        unit: "g",
      });
      this.selectedNewConstituent = null;
      this.selectShown.push(false);
    },
    turnOnRowSelect(index) {
      this.selectShown[index] = true;
      this.selectedChangedConstituent = this.constituents[index].item;
      this.$nextTick(function () {
        // unfortunately this seems to be the "official" way to focus on the select element:
        this.$refs[`select${index}`].$refs.selectComponent.$refs.search.focus();
      });
    },
    swapConstituent(selectedItem, index) {
      this.constituents[index].item = selectedItem;
      this.selectShown[index] = false;
    },
    removeConstituent(index) {
      this.constituents.splice(index, 1);
      this.selectShown.splice(index, 1);
    },
  },
};
</script>

<style scoped>
.subheading {
  color: darkslategrey;
  font-size: small;
  font-weight: 600;
  text-transform: uppercase;
  margin-bottom: 0px;
}
</style>
