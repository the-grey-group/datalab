<template>
  <div>
    <div v-if="isSampleFetchError" class="alert alert-danger">
      Server Error. Sample list not retreived.
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
import FormattedItemName from "@/components/FormattedItemName";
import ChemicalFormula from "@/components/ChemicalFormula";
import CollectionList from "@/components/CollectionList";
import Creators from "@/components/Creators";
import { h, getCurrentInstance } from "vue";

const FormattedItemNameAg = {
  setup(props) {
    const { params } = props;
    return () =>
      h(FormattedItemName, {
        item_id: params.value,
        "item-type": params.data.type,
        "enable-modified-click": true,
      });
  },
};

const ChemicalFormulaAg = {
  setup(props) {
    const { params } = props;
    return () => h(ChemicalFormula, { formula: params.value });
  },
};

const IsoDatetimeToDateAg = {
  setup(props) {
    const instance = getCurrentInstance();
    const { params } = props;
    const filters = instance.appContext.config.globalProperties.$filters;

    return () => h("span", filters.IsoDatetimeToDate(params.value));
  },
};

const CollectionListAg = {
  setup(props) {
    const { params } = props;
    return () => h(CollectionList, { collections: params.value });
  },
};

const CreatorsAg = {
  setup(props) {
    const { params } = props;
    return () =>
      h(Creators, {
        creators: params.value,
      });
  },
};

export default {
  components: {
    AgGridVue,
    // eslint-disable-next-line
    FormattedItemNameAg,
    // eslint-disable-next-line
    ChemicalFormulaAg,
    // eslint-disable-next-line
    IsoDatetimeToDateAg,
    // eslint-disable-next-line
    CollectionListAg,
    // eslint-disable-next-line
    CreatorsAg,
  },
  setup() {
    return {
      isSampleFetchError: false,
      searchValue: "",
      itemsSelected: [],
      columnDefs: [
        {
          headerName: "ID",
          field: "item_id",
          cellRenderer: "FormattedItemNameAg",
          checkboxSelection: true,
          headerCheckboxSelection: true,
          // floatingFilter: true,
          flex: 2,
        },
        { headerName: "Type", field: "type", flex: 1 },
        { headerName: "Sample name", field: "name", flex: 1 },
        { headerName: "Formula", field: "chemform", cellRenderer: "ChemicalFormulaAg", flex: 1 },
        {
          headerName: "Date",
          field: "date",
          cellRenderer: "IsoDatetimeToDateAg",
          flex: 1,
        },
        {
          headerName: "Collections",
          field: "collections",
          cellRenderer: "CollectionListAg",
          valueFormatter: (params) => {
            return Object.values(params.value);
          },
          flex: 1,
        },
        {
          headerName: "Creators",
          field: "creators",
          cellRenderer: "CreatorsAg",
          valueFormatter: (params) => {
            return Object.values(params.value);
          },
          flex: 1,
        },
        { headerName: "# of blocks", field: "nblocks", flex: 1 },
      ],
      rowSelection: "multiple",
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
