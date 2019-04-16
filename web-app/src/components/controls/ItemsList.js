import React from 'react'
import { Item } from 'semantic-ui-react'

const ItemsList = ({items}) => (
    <Item.Group>
        {items.map(item =>
            <Item>
                <Item.Content>
                    <Item.Header as='a'>{item.title}</Item.Header>
                    <Item.Description>
                        <p>{item.content}</p>
                    </Item.Description>
                </Item.Content>
            </Item>
        )}
    </Item.Group>
);

export default ItemsList