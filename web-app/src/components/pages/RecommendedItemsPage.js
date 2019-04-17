import React from 'react';
import { connect } from 'react-redux';
import ItemsList from '../controls/ItemsList'

class RecommendedItemsPage extends React.Component {
    render() {
        return (<ItemsList items={this.props.recommendedItems}/>);
    }
}

function mapStateToProps(state) {
    return {
        recommendedItems: state.recommendedItems,
    };
}

export default connect(mapStateToProps)(RecommendedItemsPage);