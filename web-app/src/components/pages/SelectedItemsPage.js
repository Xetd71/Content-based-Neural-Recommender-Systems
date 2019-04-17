import React from 'react';
import { connect } from 'react-redux';
import ItemsList from '../controls/ItemsList'

class SelectedItemsPage extends React.Component {
    render() {
        return (<ItemsList items={this.props.userItems}/>);
    }
}

function mapStateToProps(state) {
    return {
        userItems: state.userItems,
    };
}

export default connect(mapStateToProps)(SelectedItemsPage);