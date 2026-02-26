export function Button({
  children,
  variant = 'primary',
  size = 'md',
  className = '',
  ...props
}) {
  const baseClasses = 'font-semibold rounded-lg border-2 transition-all duration-300 cursor-pointer hover:shadow-lg';

  const variants = {
    primary: 'bg-alc-magenta border-alc-magenta text-white hover:bg-alc-purple hover:border-alc-purple',
    secondary: 'bg-transparent border-alc-cyan text-alc-cyan hover:bg-alc-cyan hover:text-alc-dark',
    accent: 'bg-alc-cyan border-alc-cyan text-alc-dark hover:bg-alc-light-blue hover:border-alc-light-blue',
    outline: 'bg-transparent border-alc-light-blue text-alc-light-blue hover:bg-alc-light-blue hover:text-alc-dark',
  };

  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  const buttonClasses = `${baseClasses} ${variants[variant]} ${sizes[size]} ${className}`;

  return (
    <button className={buttonClasses} {...props}>
      {children}
    </button>
  );
}
