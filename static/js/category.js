Vue.component('transaction-category-list', {
    data() {
      return {
        categories: [],
      };
    },
    methods: {
      fetchCategories() {
        axios.get('/myapp/api/transaction_categories/')
          .then(response => {
            this.categories = response.data;
          });
      },
    },
    created() {
      this.fetchCategories();
    },
    template: `
      <div>
        <ul>
          <li v-for="category in categories" :key="category.uuid">{{ category.name }}</li>
        </ul>
      </div>
    `,
  });