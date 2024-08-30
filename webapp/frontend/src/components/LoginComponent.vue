<script>
import axios from 'axios';

export default {
  methods: {
    async login() {
      try {
        const response = await axios.post('/auth/login', {
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
