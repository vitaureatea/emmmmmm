import React from 'react';
import ReactDOM from 'react-dom';
import Get_opsdoc_body from "../service/get_opsdoc_body";


export default class GetBody extends React.Component {

    constructor (props) {
        super(props);
        this.state={
            body:[],
            title:this.props.match.params.name
        };
        this.service = new Get_opsdoc_body();
        this.service.doc_body(this)
    }

    render () {
        return (
            <pre>
                2134123512
                1235sadf
                hasdf
            </pre>
        )
    }
}
