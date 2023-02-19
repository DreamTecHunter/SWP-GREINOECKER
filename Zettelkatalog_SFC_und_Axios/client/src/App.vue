<template>
  <h1>Zettelkatalog</h1>
  <h2>Suche</h2>
  <input v-model="word"/>
  <button @click="get_cards(word)">search</button>
  <table>
    <tr v-for="card in cards">
      <td>
        <button @click="edit_card(card.id)">edit {{ card.id }}</button>
      </td>
      <td>{{ card.thumb }}</td>
      <td><img src="{{card.thumb}}"></td>
      <td>{{ card.description }}</td>

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
      cards: {}

    }
  },
  methods:
      {
        async get_cards(word) {
          const responds = await axios.get(`http://127.0.0.1:5000/cat-search/${word}`, {})
          this.cards = responds.data
          this.cards = this.cards.map(c => c.replace(word, "<b>" + word + "</b>"))
          console.log(this.cards)
        },
        edit_card(card) {

        }
      }
}
</script>

