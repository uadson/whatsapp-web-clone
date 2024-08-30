<script>
import axios from 'axios';

export default {
  methods: {
    async register() {
      try {
        const response = await axios.post('/users/', {
          username: this.username,
          password: this.password,
        });
        // Use a resposta, por exemplo:
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>
