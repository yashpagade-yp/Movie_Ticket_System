import * as React from 'react';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
    ({ className = '', label, error, type, ...props }, ref) => {
        return (
            <div className="w-full">
                {label && (
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        {label}
                    </label>
                )}
                <input
                    type={type}
                    className={`
            flex h-11 w-full rounded-lg border bg-white px-4 py-2 text-sm
            transition-all duration-200
            placeholder:text-gray-400
            focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent
            disabled:cursor-not-allowed disabled:opacity-50
            ${error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300'}
            ${className}
          `}
                    ref={ref}
                    {...props}
                />
                {error && (
                    <p className="mt-1 text-sm text-red-500">{error}</p>
                )}
            </div>
        );
    }
);
Input.displayName = 'Input';

export { Input };
