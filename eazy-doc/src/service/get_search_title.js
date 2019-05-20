import axios from "axios";


export default class Get_search_title {

    search_title(_this) {
        axios.get('/doc/document/search/', {
            params: {search: _this.search}
        }).then(response => {
            console.log('2222222',response.data.body);
            _this.setState({
                body:response.data.body,
                title:response.data.title
            });
        })
            .catch(error => {

            });
    }
}

