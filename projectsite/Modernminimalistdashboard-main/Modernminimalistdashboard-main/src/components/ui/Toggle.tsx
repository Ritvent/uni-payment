interface ToggleProps {
  options: string[];
  active: string;
  onChange: (option: string) => void;
}

export function Toggle({ options, active, onChange }: ToggleProps) {
  return (
    <div className="inline-flex bg-white border border-gray-200 rounded-lg p-1">
      {options.map((option) => (
        <button
          key={option}
          onClick={() => onChange(option)}
          className={`px-6 py-2 rounded-md transition-colors ${
            active === option
              ? 'bg-gray-900 text-white'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          {option}
        </button>
      ))}
    </div>
  );
}
