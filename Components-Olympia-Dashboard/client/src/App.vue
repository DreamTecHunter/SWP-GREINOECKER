<template>
  <header>
    <h1>Hello</h1>
  </header>

  <main>
    <h2>Hello back</h2>
    <DataTable class="table table-hover table-striped" width="100%" :data="medals">
      <thead>
      <tr>
        <th v-for="c in words">{{ c }}</th>
      </tr>
      </thead>
      <tfoot>

      </tfoot>
    </DataTable>
  </main>
</template>

<style>
@import "bootstrap";
@import "datatables.net-bs5";
</style>

<script setup>
import DataTable from 'datatables.net-vue3'
import DataTablesLib from 'datatables.net-bs5'
import axios from 'axios'

export default {
  data() {
    return {
      columns: [],
      medals: []
    }
  },
  methods:
      {
        setup() {
          console.log("setup");
          DataTable.use(DataTablesLib);
          this.columns = this.get_columns()
          this.medals = this.get_medals()
        },
        async get_columns() {
          const _columns = await axios.get(`http://127.0.0.1:5000/get_columns`, {})
          const _columns_data = columns.data
          console.log(_columns_data)
          return _columns_data
        },
        async get_medals() {
          const _medals = await axios.get(`http://127.0.0.1:5000/medals/${'AUT'}`)
          const _medals_data = medals.data
          console.log(medals)
          return _medals_data
        }
      }
}
</script>