import React from "react";
import PropTypes from "prop-types";

const NoMatchPage = ({ location }) => (
    <div>
        <h3>
            No match for <code>{location.pathname}</code>
        </h3>
    </div>
);

NoMatchPage.propTypes = {
    location: PropTypes.shape({
        pathname: PropTypes.string.isRequired
    }).isRequired,
};

export default NoMatchPage