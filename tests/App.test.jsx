import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '../src/App';

describe('PRISM 9 App Interface', () => {
  it('renders main header branding', () => {
    render(<App />);
    expect(screen.getByText('PRISM 9')).toBeInTheDocument();
  });

  it('displays active status indicators', () => {
    render(<App />);
    expect(screen.getByText(/Cache:/i)).toBeInTheDocument();
    expect(screen.getByText(/Document Ingestion Gateway/i)).toBeInTheDocument();
  });

  it('renders 9SM Substrate Matrix control panel', () => {
    render(<App />);
    expect(screen.getByText('9SM Substrate Matrix')).toBeInTheDocument();
    expect(screen.getByText('Financial Alpha')).toBeInTheDocument();
  });
});
