<template>
    <div>
      <h1>Busca de todas as Operadoras cadastradas</h1>
      <button>Buscar</button>
      <ul>
        <li v-for="result in results" :key="result.id">{{ result.name }}</li>
      </ul>
    </div>

    <div>
      <h1>Buscar Operadoras por CNPJ</h1>
      <input v-model="query" @input="search" placeholder="Digite o CNPJ da operadora" />
      <ul>
        <li v-for="result in results" :key="result.id">{{ result.name }}</li>
      </ul>
      <button>Buscar</button>
    </div>

    <div>
      <h1>Busca Avançada</h1>
      <h3>Periodo</h3>
      <h3>Razão Social</h3>
      <h3>Registro ANS</h3>
      <button>Buscar</button>
      <ul>
        <li v-for="result in results" :key="result.id">{{ result.name }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        query: '',
        results: []
      };
    },
    methods: {
      async search() {
        if (this.query.length > 2) {
          const response = await fetch(`https://api.exemplo.com/search?q=${this.query}`);
          this.results = await response.json();
        } else {
          this.results = [];
        }
      }
    }
  };
  </script>
  
  <style>
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
  }
  </style>