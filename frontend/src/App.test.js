import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import App from './App';

const setup = () => {
    render(
        <BrowserRouter>
            <App />
        </BrowserRouter>
    );
}

test('Renders title of main page', () => {
    setup();
    const titleElement = screen.getByText(/Kvalitetssikring/i);
    expect(titleElement).toBeInTheDocument();
});


test('Navigate to Object Level Target page and back to main page', () => {
    setup();
    const leftClick = { button: 0 }
    userEvent.click(screen.getByText(/Object Level Target/i), leftClick)
    const titleElement = screen.getByText(/Object Level Target/);
    expect(titleElement).toBeInTheDocument();
    userEvent.click(screen.getByText(/Cancel/i), leftClick)
    expect(screen.getByText(/Kvalitetssikring/)).toBeInTheDocument();
})

test('Navigate to Device Level Target page and back to main page', () => {
    setup();
    const leftClick = { button: 0 }
    userEvent.click(screen.getByText(/Device Level Target/i), leftClick)
    const titleElement = screen.getByText(/Device Level Target/);
    expect(titleElement).toBeInTheDocument();
    userEvent.click(screen.getByText(/Cancel/i), leftClick)
    expect(screen.getByText(/Kvalitetssikring/)).toBeInTheDocument();
})
