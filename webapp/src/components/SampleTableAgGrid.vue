<template>
  <div>
    <div v-if="isSampleFetchError" class="alert alert-danger">
      Server Error. Sample list not retreived.
    </div>

    <div class="form-inline mb-2 ml-auto">
      <button
        class="btn btn-default ml-auto mr-2"
        :disabled="!Boolean(itemsSelected.length)"
        @click="deleteSelectedItems"
      >
        Delete selected...
      </button>
      <div class="form-group">
        <label for="sample-table-search" class="sr-only">Search items</label>
        <input
          id="sample-table-search"
          type="text"
          class="form-control"
          v-model="searchValue"
          placeholder="search"
          @input="applyFilter"
        />
      </div>
    </div>

    <ag-grid-vue
      class="ag-theme-alpine customize-table"
      :columnDefs="columnDefs"
      :rowData="samples"
      :rowSelection="rowSelection"
      @rowClicked="goToEditPage"
      @selectionChanged="onSelectionChanged"
      :pagination="true"
      :paginationPageSize="10"
      :domLayout="'autoHeight'"
      :defaultColDef="defaultColDef"
      style="width: 100%; height: 400px"
    ></ag-grid-vue>
  </div>
</template>

<script>
import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { getSampleList, deleteSample } from "@/server_fetch_utils.js";

export default {
  components: {
    AgGridVue,
  },
  data() {
    return {
      isSampleFetchError: false,
      searchValue: "",
      itemsSelected: [],
      columnDefs: [
        {
          headerName: "ID",
          field: "item_id",
          checkboxSelection: true,
          headerCheckboxSelection: true, // Allow header checkbox to select/deselect all rows
          sortable: true,
          filter: true,
          floatingFilter: true,
        },
        { headerName: "Type", field: "type" },
        { headerName: "Sample name", field: "name" },
        { headerName: "Formula", field: "chemform" },
        { headerName: "Date", field: "date" },
        { headerName: "Collection", field: "collection" },
        { headerName: "Creators", field: "creators" },
        { headerName: "# of blocks", field: "nblocks" },
      ],
      rowSelection: "multiple", // Enable multiple row selection
      defaultColDef: {
        resizable: true,
        sortable: true,
        filter: true,
      },
    };
  },
  computed: {
    samples() {
      return this.$store.state.sample_list;
    },
  },
  methods: {
    goToEditPage(params) {
      const row = params.data;
      const event = params.event;
      if (event.ctrlKey || event.metaKey || event.altKey) {
        window.open(`/edit/${row.item_id}`, "_blank");
      } else {
        this.$router.push(`/edit/${row.item_id}`);
      }
    },
    getSamples() {
      getSampleList()
        .then(() => {
          console.log("sample list received!");
        })
        .catch(() => {
          this.isSampleFetchError = true;
        });
    },
    applyFilter() {
      this.gridOptions.api.setQuickFilter(this.searchValue);
    },
    onSelectionChanged(event) {
      this.itemsSelected = event.api.getSelectedRows();
    },
    deleteSelectedItems() {
      const idsSelected = this.itemsSelected.map((x) => x.item_id);
      if (
        confirm(
          `Are you sure you want to delete ${this.itemsSelected.length} selected items (${idsSelected})?`,
        )
      ) {
        idsSelected.forEach((item_id) => {
          deleteSample(item_id);
        });
      }
    },
  },
  mounted() {
    this.getSamples();
  },
};
</script>

<style>
.customize-table .ag-header {
  font-size: 1rem;
}
</style>
