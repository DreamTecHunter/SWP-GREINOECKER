<template>
  <h1>Zettelkatalog</h1>

  <h2>Editierbereich</h2>
  <table>
    <tr>
      <td>
        <img src="{{thumb}}"/>
      </td>
      <td>
        <label>{{ version }}</label>
        <br>
        <textarea style="width: 512px; height: 128px" v-model="description"></textarea>
      </td>
      <td>
        <button @click="send_change_card()">change</button>
      </td>
    </tr>
  </table>

  <h2>Suche</h2>
  <input v-model="word"/>
  <button @click="get_cards(word)">search</button>
  <table>
    <tr v-for="card in cards">
      <td>
        <button @click="edit_card(card)">edit {{ card.id }}</button>
      </td>
      <td>
        {{ card.thumb }}
      </td>
      <td>
        <img src="{{card.thumb}}"/>
      </td>
      <td>
        {{ card.description }}
      </td>
    </tr>
  </table>

</template>

<style scoped>
</style>


<script>
import CCAHeader from './components/CCAHeader.vue'
import BlogEntry from './components/BlogEntry.vue'
import axios from "axios";


export default {
  components:
      {
        CCAHeader, BlogEntry
      },
  data() {
    return {
      word: '',
      cards: {},
      thumb: '',
      id: '',
      description: '',
      version: ''
    }
  },
  methods:
      {
        async get_cards(word) {
          const responds = await axios.get(`http://127.0.0.1:5001/cat-search/${word}`, {})

          this.cards = responds.data
          console.log("Request " + responds.statusText)
        },
        async edit_card(card) {
          this.thumb = card.thumb
          this.id = card.id
          this.description = card.description
          this.version = await this.get_version(card.id)
          console.log("Button: Edit clicked")
        },
        async send_change_card(){
          await this.send_change_card_catalog()
          await this.send_change_card_history()
        },
        async send_change_card_catalog() {
          const responds = await axios.patch(`http://127.0.0.1:5001/cat-item/${this.id}`, {
            params: {
              description: this.description,
              card_id: this.id
            }
          });
          console.log("Patch " + responds.statusText)
        },
        async send_change_card_history() {
          const responds = await axios.put(`http://127.0.0.1:5002/card-item/${this.id}`, {
            params: {
              description: this.description,
              datetime: Date.now().toString()
            }
          });
          console.log("Patch " + responds.statusText)
        },
        async get_version(id) {
          const responds = await axios.get(`http://127.0.0.1:5002/card-search/${id}`, {})
          return responds.data[responds.data.length-1].datetime
        }
      }
}
</script>

