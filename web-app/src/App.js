import React, { Component } from 'react'
import { Route, Switch, Redirect } from "react-router-dom";
import { Container, Dropdown, Menu, Visibility, Input } from 'semantic-ui-react'
import PropTypes from "prop-types";
import { connect } from 'react-redux';
import { ItemsPage, SelectedItemsPage, RecommendedItemsPage, NoMatchPage } from "./components/pages/";
import { setUserId, setAlgorithm } from './actions/setProperties';

const menuStyle = {
    border: 'none',
    borderRadius: 0,
    boxShadow: 'none',
    marginBottom: '1em',
    marginTop: '1em',
    transition: 'box-shadow 0.5s ease, padding 0.5s ease',
};

const fixedMenuStyle = {
    // backgroundColor: '#fff',
    border: '1px solid #ddd',
    marginBottom: '1em',
    // boxShadow: '0px 3px 5px rgba(0, 0, 0, 0.2)',
};

const isNumber = new RegExp('^\\d*$');

class App extends Component {
    constructor(props) {
        super(props);
        props.setUserId(0);
        props.setAlgorithm(0, 'ALS');
        this.state = {
            menuFixed: false,
            location: window.location.pathname,
            typedUserId: '',
            maxUserId: 42976,
        };
    }



    changeLink = (e, { name }) => {
        this.props.history.push(name);
        this.setState({ location: name})
    };

    selectAlgorithm = (e, {name}) => {
        this.props.setAlgorithm(this.props.userId, name);
    };

    changeUser = (e) => {
        if(isNumber.test(e.target.value)) {
            const typedUserId = e.target.value === '' ? '' : Math.min(parseInt(e.target.value, 10), this.state.maxUserId);
            this.props.setUserId(typedUserId === '' ? 0 : typedUserId);
            this.setState({typedUserId: typedUserId});
        }
    };

    stickTopMenu = () => this.setState({ menuFixed: true });

    unStickTopMenu = () => this.setState({ menuFixed: false });

    render() {
        const { menuFixed, location, typedUserId } = this.state;
        const { algorithm } = this.props;
        return (
            <div>
                <Visibility onBottomPassed={this.stickTopMenu} onBottomVisible={this.unStickTopMenu} once={false}>
                    <Menu borderless fixed={menuFixed ? 'top' : undefined} style={menuFixed ? fixedMenuStyle : menuStyle}>
                        <Container text>
                            {/*<Menu.Item as='a' name="/items" active={location === "/items"} onClick={this.changeLink}>*/}
                            {/*    Items*/}
                            {/*</Menu.Item>*/}
                            <Menu.Item as='a' name="/selected-items" active={location === "/selected-items"} onClick={this.changeLink}>
                                Selected Items
                            </Menu.Item>
                            <Menu.Item as='a' name="/recommendation" active={location === "/recommendation"} onClick={this.changeLink}>
                                Recommendation
                            </Menu.Item>
                            <Menu.Item position='right' name="user">
                                <Input label='User:' value={typedUserId} placeholder='0' onChange={this.changeUser} style={{maxWidth: '5em'}} />
                            </Menu.Item>
                            <Menu.Menu position='right'>
                                <Dropdown text={algorithm ? 'Algorithm: ' + algorithm : 'Algorithm'} pointing className='link item'>
                                    <Dropdown.Menu>
                                        <Dropdown.Item name="ALS" onClick={this.selectAlgorithm}>ALS</Dropdown.Item>
                                        <Dropdown.Item name="DSSM" onClick={this.selectAlgorithm}>DSSM</Dropdown.Item>
                                    </Dropdown.Menu>
                                </Dropdown>
                            </Menu.Menu>
                        </Container>
                    </Menu>
                </Visibility>

                <Container text style={{marginBottom: '2em'}}>
                    <Switch>
                        <Redirect exact from="/" to="/selected-items"/>
                        <Route exact path="/items" component={ItemsPage}/>
                        <Route exact path="/selected-items" component={SelectedItemsPage}/>
                        <Route exact path="/recommendation" component={RecommendedItemsPage}/>
                        <Route component={NoMatchPage}/>
                    </Switch>
                </Container>


            </div>
        )
    }
}

App.propTypes = {
    history: PropTypes.shape({
        push: PropTypes.func.isRequired
    }).isRequired,
    setUserId: PropTypes.func.isRequired,
    setAlgorithm: PropTypes.func.isRequired,
};

function mapStateToProps(state) {
    return {
        userId: state.userId,
        algorithm: state.algorithm,
    }
}


export default connect(mapStateToProps, {setUserId, setAlgorithm})(App);
