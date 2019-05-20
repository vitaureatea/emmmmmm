import axios from "axios";


export default class Get_opsdoc_body {

    doc_body(_this){
        axios.get('/doc/document/ops_body/', {
            params:{title: _this.title}
        }).then(response => {
                console.log('11111111',response.data.body);
                _this.setState({
                    body:response.data.body
                });
            })
            .catch(error => {

            });
    }
}
