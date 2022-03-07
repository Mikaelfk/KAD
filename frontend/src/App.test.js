import { render, screen } from '@testing-library/react';
import App from './App';
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom';

test('renders title of main page', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const titleElement = screen.getByText(/Kvalitetssikring/i);
  expect(titleElement).toBeInTheDocument();
});


test('Navigate to Object Level Target page and back to main page', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const leftClick = {button: 0}
  userEvent.click(screen.getByText(/Object Level Target/i), leftClick)
  const titleElement = screen.getByText(/Object Level Target/);
  expect(titleElement).toBeInTheDocument();
  userEvent.click(screen.getByText(/Cancel/i), leftClick)
  expect(screen.getByText(/Kvalitetssikring/)).toBeInTheDocument();
})

test('Navigate to Device Level Target page and back to main page', () => {
  render(<BrowserRouter><App /></BrowserRouter>);
  const leftClick = {button: 0}
  userEvent.click(screen.getByText(/Device Level Target/i), leftClick)
  const titleElement = screen.getByText(/Device Level Target/);
  expect(titleElement).toBeInTheDocument();
  userEvent.click(screen.getByText(/Cancel/i), leftClick)
  expect(screen.getByText(/Kvalitetssikring/)).toBeInTheDocument();
})
