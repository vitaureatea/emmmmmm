import axios from "axios";


export default class Get_opsdoc_title {

    doc_title(_this){
        axios.get('/doc/document/ops_title/')
            .then(response => {
                _this.setState({
                    title:response.data.title
                });
            })
            .catch(error => {

            });
    }
}
