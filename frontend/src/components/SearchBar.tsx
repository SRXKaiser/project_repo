import type { ChangeEvent } from 'react';

interface SearchBarProps {
  placeholder?: string;
  value: string; 
  onSearch?: (query: string) => void;
}

const SearchBar = ({
  placeholder = 'Buscar por título...',
  value,
  onSearch,
}: SearchBarProps) => {
  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    onSearch?.(e.target.value);
  };

  const handleClear = () => {
    onSearch?.('');
  };

  return (
    <div className="w-full">
      <div className="flex shadow-md rounded-[0.75em] border-2 border-[var(--rojo-oscuro)] overflow-hidden bg-[var(--bg)]/70">
        <div className="flex items-center pr-4 pl-4 text-[var(--cafe)]/60">
          <svg
            className="w-5 h-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeWidth="2"
              d="m21 21-3.5-3.5M17 10a7 7 0 1 1-14 0 7 7 0 0 1 14 0Z"
            />
          </svg>
        </div>

        <input
          type="search"
          value={value}
          onChange={handleChange}
          placeholder={placeholder}
          className="px-3 py-2.5 bg-[var(--bg)]/70
                     text-[var(--text-h)] text-sm
                     focus:outline-none
                     block w-full placeholder:text-[var(--cafe)]/60
                     transition"
        />

        {value && (
          <button
            type="button"
            onClick={handleClear}
            aria-label="Limpiar búsqueda"
            className="flex items-center px-3 text-[var(--cafe)]/60
                       hover:text-[var(--rojo)] transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18 18 6M6 6l12 12"
              />
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default SearchBar;