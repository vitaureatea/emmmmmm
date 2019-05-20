import React from 'react';
import ReactDOM from 'react-dom';
import 'antd/dist/antd.css';
import './index.css';
import 'bootstrap/dist/css/bootstrap.css';
import {
    Layout, Menu, Breadcrumb, Icon,
} from 'antd';
import $ from 'jquery';

import Get_opsdoc_title from './service/get_opsdoc_title';
import Get_opsdoc_body from "./service/get_opsdoc_body";
import Get_search_title from "./service/get_search_title";


const {
    Header, Content, Footer, Sider,
} = Layout;
const SubMenu = Menu.SubMenu;

class DocTitle extends React.Component {

    constructor (props) {
        super(props);
        this.state={
            title:[],
            body:[]
        };
        this._service = new Get_opsdoc_body;
        this.search_service = new Get_search_title;
        this.service = new Get_opsdoc_title();
        this.service.doc_title(this);

    }

    handleClick(event){
        console.log(event.key);
        this.title = event.key;
        this._service.doc_body(this)
    }

    searchvalue(event){
        console.log(event.target.value);
        this.search = event.target.value;
        this.search_service.search_title(this)
    }

    state = {
        collapsed: false,
    };

    onCollapse = (collapsed) => {
        console.log(collapsed);
        this.setState({ collapsed });
    };


    render() {
        const data = () => {
            return this.state.title
        };

        const ht = () => {
            var res = [];
            for(var i = 0; i < data().length; i++){
                res.push(<Menu.Item key={data()[i]}><Icon type="file" /><span >{data()[i]}</span></Menu.Item>)
            }

            return res
        };

        return (
            <Layout style={{ minHeight: '100vh' }}>

                <Sider
                    collapsible
                    collapsed={this.state.collapsed}
                    onCollapse={this.onCollapse}
                >
                    <div className="logo">
                        <div className="input-group">
                            <input type="text" className="form-control" placeholder='搜索' onChange={this.searchvalue.bind(this)}></input>
                        </div>
                        </div>
                    <Menu onClick={this.handleClick.bind(this)} theme="dark" defaultSelectedKeys={['1']} mode="inline">
                        {ht()}
                    </Menu>
                </Sider>
                <Layout>
                    <Header style={{ background: '#fff', padding: 0 }} >
                        <div className="row">
                            <div className="col-md-2"></div>
                            <div className="col-sm-12">
                            <div className="col-md-10">
                                <div className="btn-group" role="group" aria-label="...">
                                    <button type="button" className="btn btn-default">新建文档</button>
                                    <button type="button" className="btn btn-default">删除当前文档</button>
                                    <button type="button" className="btn btn-default">编辑当前文档</button>
                                </div>
                            </div>
                            </div>
                        </div>
                    </Header>
                    <Content style={{ margin: '0 16px' }}>
                        <Breadcrumb style={{ margin: '16px 0' }}>
                        </Breadcrumb>
                        <div style={{ padding: 24, background: '#fff', minHeight: 650 }} id={'doc'}>
                            {this.state.body}
                        </div>
                    </Content>
                    <Footer style={{ textAlign: 'center' }}>
                        Ant Design ©2018 Created by Ant UED
                    </Footer>
                </Layout>
            </Layout>
        );
    }
}

ReactDOM.render(<DocTitle />, document.getElementById('root'));
