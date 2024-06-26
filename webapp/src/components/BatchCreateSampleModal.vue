<template>
  <form data-testid="batch-modal-container" class="modal-enclosure" @submit.prevent="submitForm">
    <Modal
      :model-value="modelValue"
      :disable-submit="
        sampleIDValidationMessages.some((e) => e) ||
        (!generateIDsAutomatically && samples.some((s) => !Boolean(s.item_id)))
      "
      @update:model-value="$emit('update:modelValue', $event)"
    >
      <template #header>
        <template v-if="beforeSubmit">Add new samples</template>
        <template v-else>
          <a id="back-arrow" role="button" @click="beforeSubmit = true">←</a>
          Samples added
        </template>
      </template>
      <template #body>
        <div id="screens-container">
          <transition name="slide-content-left">
            <div v-show="beforeSubmit" id="left-screen">
              <div class="row">
                <div class="col-md-8 mt-2" @click="templateIsOpen = !templateIsOpen">
                  <font-awesome-icon
                    :icon="['fas', 'chevron-right']"
                    fixed-width
                    class="collapse-arrow clickable"
                    :class="{ expanded: templateIsOpen }"
                  />
                  <label class="blue-label clickable pl-2"> Template: </label>
                </div>
                <label
                  for="batchSampleNRows"
                  class="blue-label col-md-2 col-3 col-form-label text-left mb-2"
                >
                  Number of rows:
                </label>
                <input
                  id="batchSampleNRows"
                  v-model="nSamples"
                  class="form-control col-md-1 col-2"
                  type="number"
                  min="0"
                  max="100"
                />
              </div>

              <div
                v-show="templateIsOpen"
                class="card bg-light mt-2 mx-auto mb-4"
                style="width: 95%"
              >
                <table data-testid="batch-add-table-template" class="table table-sm mb-2">
                  <thead>
                    <tr class="subheading template-subheading">
                      <th style="width: calc(12%)">ID</th>
                      <th>Name</th>
                      <th style="width: calc(15%)">Date</th>
                      <th style="width: calc(22%)">Copy from</th>
                      <th style="width: calc(22%)">Components</th>
                    </tr>
                  </thead>
                  <tbody>
                    <td>
                      <input
                        v-model="sampleTemplate.item_id"
                        class="form-control"
                        :placeholder="generateIDsAutomatically ? null : 'ex_{#}'"
                        :disabled="generateIDsAutomatically"
                        @input="applyIdTemplate"
                      />
                      <div class="form-check mt-1 ml-1">
                        <input
                          id="automatic-batch-id-label"
                          v-model="generateIDsAutomatically"
                          type="checkbox"
                          class="form-check-input clickable"
                          @input="setIDsNull"
                        />
                        <label
                          id="automatic-id-label"
                          class="form-check-label clickable"
                          for="automatic-batch-id-label"
                        >
                          auto IDs
                        </label>
                      </div>
                    </td>
                    <td>
                      <input
                        v-model="sampleTemplate.name"
                        class="form-control"
                        placeholder="Example name {#}"
                        @input="applyNameTemplate"
                      />
                    </td>
                    <td>
                      <input
                        v-model="sampleTemplate.date"
                        class="form-control"
                        type="datetime-local"
                        :min="epochStart"
                        :max="oneYearOn"
                        @input="applyDateTemplate"
                      />
                    </td>
                    <td>
                      <ItemSelect
                        v-model="sampleTemplate.copyFrom"
                        :formatted-item-name-max-length="8"
                        @update:model-value="applyCopyFromTemplate"
                      />
                    </td>
                    <td>
                      <ItemSelect
                        v-model="sampleTemplate.components"
                        multiple
                        :formatted-item-name-max-length="8"
                        @update:model-value="applyComponentsTemplate"
                      />
                    </td>
                  </tbody>
                </table>

                <div class="form-group mt-2 mb-1" style="display: flex">
                  <label
                    id="start-counting-label"
                    for="start-counting"
                    class="px-3 col-form-label-sm"
                  >
                    start counting {#} at:
                  </label>
                  <input
                    id="start-counting"
                    v-model="templateStartNumber"
                    type="number"
                    class="form-control form-control-sm"
                    style="width: 5em"
                    @input="applyIdAndNameTemplates"
                  />
                </div>
              </div>

              <table data-testid="batch-add-table" class="table mb-2">
                <thead>
                  <tr class="subheading">
                    <th style="width: calc(12%)">ID</th>
                    <th>Name</th>
                    <th style="width: calc(15%)">Date</th>
                    <th style="width: calc(22%)">Copy from</th>
                    <th style="width: calc(22%) - 2rem">Components</th>
                    <th style="width: 2rem"></th>
                  </tr>
                </thead>
                <tbody>
                  <template v-for="(sample, index) in samples" :key="index">
                    <tr>
                      <td>
                        <input
                          v-model="sample.item_id"
                          class="form-control"
                          :disabled="generateIDsAutomatically"
                          @input="sampleTemplate.item_id = ''"
                        />
                      </td>
                      <td>
                        <input
                          v-model="sample.name"
                          class="form-control"
                          @input="sampleTemplate.name = ''"
                        />
                      </td>
                      <td>
                        <input
                          v-model="sample.date"
                          class="form-control"
                          type="datetime-local"
                          :min="epochStart"
                          :max="oneYearOn"
                        />
                      </td>
                      <td>
                        <ItemSelect v-model="sample.copyFrom" :formatted-item-name-max-length="8" />
                      </td>
                      <td>
                        <ItemSelect
                          v-model="sample.components"
                          multiple
                          :formatted-item-name-max-length="8"
                        />
                      </td>
                      <td>
                        <button
                          type="button"
                          class="close"
                          aria-label="delete"
                          @click.stop="removeRow(index)"
                        >
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </td>
                    </tr>
                    <td colspan="3">
                      <!-- eslint-disable-next-line vue/no-v-html -->
                      <span class="form-error" v-html="sampleIDValidationMessages[index]" />
                    </td>
                  </template>
                </tbody>
              </table>
            </div>
          </transition>
          <transition name="slide-content-right">
            <div v-show="!beforeSubmit" id="right-screen">
              <div v-for="(response, index) in serverResponses" :key="index">
                <div v-if="response.status == 'success'" class="callout callout-info">
                  <a class="item-id-link" :href="`edit/${response.item_id}`">
                    {{ response.item_id }}
                  </a>
                  Successfully created.
                </div>
                <div
                  v-if="
                    response.status == 'error' &&
                    response.message.includes('item_id_validation_error')
                  "
                  class="callout callout-danger form-error"
                >
                  <a :href="`edit/${response.item_id}`">
                    {{ response.item_id }}
                  </a>
                  was not added as it already exists in the database.
                </div>
                <div v-else-if="response.status == 'error'" class="callout callout-danger">
                  {{ response.message }}
                </div>
              </div>
            </div>
          </transition>
        </div>
      </template>
      <template v-if="!beforeSubmit" #footer>
        <button type="button" class="btn btn-info" @click="openEditPagesInNewTabs">Open all</button>
        <button
          type="button"
          class="btn btn-secondary"
          data-dismiss="modal"
          @click="$emit('update:modelValue', false)"
        >
          Close
        </button>
      </template>
    </Modal>
  </form>
</template>

<script>
import Modal from "@/components/Modal.vue";
import ItemSelect from "@/components/ItemSelect.vue";
import { createNewSamples } from "@/server_fetch_utils.js";
export default {
  name: "BatchCreateSampleModal",
  components: {
    Modal,
    ItemSelect,
  },
  props: {
    modelValue: Boolean,
  },
  emits: ["update:modelValue"],
  data() {
    return {
      beforeSubmit: true,
      epochStart: new Date("1970-01-01").toISOString().slice(0, -8),
      oneYearOn: this.determineOneYearOn(),
      nSamples: 3,
      generateIDsAutomatically: false,
      samples: [
        {
          item_id: null,
          name: "",
          copyFrom: null,
          components: [],
          date: this.now(),
        },
        {
          item_id: null,
          name: "",
          copyFrom: null,
          components: [],
          date: this.now(),
        },
        {
          item_id: null,
          name: "",
          copyFrom: null,
          components: [],
          date: this.now(),
        },
      ],
      takenItemIds: [], // this holds ids that have been tried, whereas the computed takenSampleIds holds ids in the sample table

      templateIsOpen: true,
      templateStartNumber: 1,
      sampleTemplate: {
        item_id: null,
        name: "",
        copyFrom: null,
        components: null,
        date: this.now(),
      },

      serverResponses: {}, // after the server responds, store error messages if any
    };
  },
  computed: {
    takenSampleIds() {
      return this.$store.state.sample_list
        ? this.$store.state.sample_list.map((x) => x.item_id)
        : [];
    },
    someValidationMessagePresent() {
      return this.sampleIDValidationMessages.some();
    },
    sampleIDValidationMessages() {
      return this.samples.map((sample, index, samples) => {
        if (sample.item_id == null) {
          return "";
        } // Don't throw an error before the user starts typing

        // check that sample id isn't repeated in this table
        if (
          samples
            .slice(0, index)
            .map((el) => el.item_id)
            .includes(sample.item_id)
        ) {
          return "ID is repeated from an above row.";
        }

        if (
          this.takenItemIds.includes(sample.item_id) ||
          this.takenSampleIds.includes(sample.item_id)
        ) {
          return `<a href='edit/${sample.item_id}'>${sample.item_id}</a> already in use.`;
        }
        if (!/^[a-zA-Z0-9._-]+$/.test(sample.item_id)) {
          return "ID can only contain alphanumeric characters, dashes ('-') and underscores ('_') and periods ('.')";
        }
        if (/^[._-]/.test(sample.item_id) | /[._-]$/.test(sample.item_id)) {
          return "ID cannot start or end with puncutation";
        }
        if (/\s/.test(sample.item_id)) {
          return "ID cannot have any spaces";
        }
        if (sample.item_id.length < 1 || sample.item_id.length > 40) {
          return "ID must be between 1 and 40 characters in length";
        }
        return "";
      });
    },
  },

  watch: {
    nSamples(newValue, oldValue) {
      if (newValue < oldValue) {
        this.samples = this.samples.slice(0, newValue);
      }
      if (newValue > oldValue) {
        for (let i = 0; i < newValue - oldValue; i++) {
          this.samples.push({ ...this.sampleTemplate });
        }
        if (this.sampleTemplate.item_id) {
          this.applyIdTemplate();
        }
        if (this.sampleTemplate.name) {
          this.applyNameTemplate();
        }
      }
    },
  },
  methods: {
    now() {
      return new Date().toISOString().slice(0, -8);
    },
    determineOneYearOn() {
      // returns a timestamp 1 year from now
      let d = new Date();
      d.setFullYear(d.getFullYear() + 1);
      return d.toISOString().slice(0, -8);
    },
    applyIdTemplate() {
      this.samples.forEach((sample, i) => {
        sample.item_id = this.sampleTemplate.item_id.replace("{#}", i + this.templateStartNumber);
      });
    },
    applyNameTemplate() {
      this.samples.forEach((sample, i) => {
        sample.name = this.sampleTemplate.name.replace("{#}", i + this.templateStartNumber);
      });
    },
    applyIdAndNameTemplates() {
      this.sampleTemplate.name && this.applyNameTemplate();
      this.sampleTemplate.item_id && this.applyIdTemplate();
    },
    applyDateTemplate() {
      this.samples.forEach((sample) => {
        sample.date = this.sampleTemplate.date;
      });
    },
    applyCopyFromTemplate() {
      this.samples.forEach((sample) => {
        sample.copyFrom = this.sampleTemplate.copyFrom;
      });
    },
    applyComponentsTemplate() {
      this.samples.forEach((sample) => {
        sample.components = this.sampleTemplate.components;
      });
    },
    removeRow(index) {
      this.samples.splice(index, 1);
      this.nSamples = this.nSamples - 1;
      // unless the removed row is the last one, reset the template and name id
      if (index != this.samples.length) {
        this.sampleTemplate.item_id = "";
        this.sampleTemplate.name = "";
      }
    },
    setIDsNull() {
      this.sampleTemplate["item_id"] = null;
      this.samples.forEach((entry) => {
        entry["item_id"] = null;
      });
    },
    async submitForm() {
      console.log("batch sample create form submit triggered");

      const newSampleDatas = this.samples.map((sample) => {
        return {
          item_id: sample.item_id,
          date: sample.date,
          name: sample.name,
          type: "samples",
          synthesis_constituents: sample.components
            ? sample.components.map((x) => ({ item: x, quantity: null }))
            : [],
        };
      });

      const copyFromItemIds = this.samples.map((sample) => sample.copyFrom?.item_id);

      await createNewSamples(newSampleDatas, copyFromItemIds, this.generateIDsAutomatically)
        .then((responses) => {
          console.log("samples added");
          this.serverResponses = responses;

          document
            .querySelector(".modal-enclosure .modal-content")
            .scrollTo({ top: 0, behavior: "smooth" });
          this.beforeSubmit = false;
        })
        .catch((error) => {
          console.log("Error with creating new samples: " + error);
        });
    },
    openEditPagesInNewTabs() {
      this.serverResponses
        .slice()
        .reverse()
        .forEach((response) => {
          window.open(`/edit/${response.item_id}`, "_blank");
        });
    },
  },
};
</script>

<style scoped>
#screens-container {
  width: 200%;
}

#left-screen {
  width: 50%;
  padding-right: 1em;
  padding-left: 1em;
  display: inline-block;
  float: left;
}

#right-screen {
  width: 50%;
  padding-left: 1em;
  display: inline-block;
  float: left;
}

#automatic-batch-id-label {
  color: #555;
}

.slide-content-left-leave-active,
.slide-content-left-enter-active {
  transition: all 0.8s ease;
}

.slide-content-left-leave-to,
.slide-content-left-enter-from {
  transform: translateX(-100%);
}

.slide-content-right-leave-active,
.slide-content-right-enter-active {
  transition: all 0.8s ease;
}

.slide-content-left-leave-active .form-error {
  display: none;
}

.slide-content-right-leave-from,
.slide-content-right-enter-to {
  transform: translateX(-100%);
}

.close {
  margin-top: 0.2em;
  color: grey;
}

.blue-label {
  font-weight: 600;
  color: #0b6093;
}

#start-counting-label {
  font-size: 1em;
  font-style: italic;
}

.template-subheading > th {
  font-style: italic;
  font-weight: 500;
}

.form-error {
  color: red;
}

:deep(.form-error a) {
  color: #820000;
  font-weight: 600;
}

.collapse-arrow {
  transition: all 0.4s;
}

.collapse-arrow:hover {
  color: #7ca7ca;
}

.expanded {
  -webkit-transform: rotate(90deg);
  -moz-transform: rotate(90deg);
  transform: rotate(90deg);
}

.item-id-link {
  color: #0b6093;
  font-weight: 600;
}

.form-error {
  color: red;
}

:deep(.form-error a) {
  color: #820000;
  font-weight: 600;
}

.modal-enclosure :deep(.modal-header) {
  padding: 0.5rem 1rem;
}

.modal-enclosure :deep(.modal-dialog) {
  max-width: 95vw;
  min-height: 90vh;
  margin-top: 2.5vh;
  margin-bottom: 2.5vh;
}

.modal-enclosure :deep(.modal-content) {
  height: 90vh;
  overflow: scroll;
  scroll-behavior: smooth;
}
</style>
