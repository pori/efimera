import React from 'react';

const Layout = ({ children }) => {
    return (
        <div className="layout">
            {/*<header>*/}
            {/*    <h1>My App</h1>*/}
            {/*</header>*/}
            <main>
                {children}
            </main>
            {/*<footer>*/}
            {/*    <p>Footer content here</p>*/}
            {/*</footer>*/}
        </div>
    );
};

export default Layout;
x