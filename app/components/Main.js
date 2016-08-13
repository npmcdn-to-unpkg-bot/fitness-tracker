var React = require('react');
var ReactDOM = require('react-dom');

var Main = React.createClass({
    render: function() {
        return (
            <div className='message'>
                <h3>the grooviest workout app for all seasons and for all reasons</h3>
                <ul>
                    <li>exercises</li>
                    <li>equipment</li>
                    <li>workouts</li>
                    <li>save, social, find?</li>
                </ul>
            </div>
        )
    }
});

ReactDOM.render(<Main />, document.getElementById('app'));
