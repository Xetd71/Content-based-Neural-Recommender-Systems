import React from 'react'
import { Item } from 'semantic-ui-react'
import PropTypes from "prop-types";

const ItemsList = ({items}) => (
    <Item.Group divided>
        {items.map(item =>
            <Item key={item.itemId}>
                <Item.Content>
                    <Item.Header>{item.title}</Item.Header>
                    <Item.Description>
                        <p>{item.content}</p>
                    </Item.Description>
                </Item.Content>
            </Item>
        )}
    </Item.Group>
);

ItemsList.propTypes = {
    items: PropTypes.arrayOf(PropTypes.shape({
        itemId: PropTypes.number,
        title: PropTypes.string,
        content: PropTypes.string

    })),
};

export default ItemsList