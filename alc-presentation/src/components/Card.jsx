export function Card({
  children,
  title,
  icon,
  className = '',
  hoverable = true,
}) {
  const hoverClass = hoverable ? 'hover:shadow-lg hover:scale-105' : '';

  return (
    <div className={`bg-alc-navy rounded-lg border border-alc-purple/30 p-6 transition-all duration-300 ${hoverClass} ${className}`}>
      {icon && (
        <div className="mb-4 flex items-center justify-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-full bg-alc-cyan/20">
            <span className="text-2xl">{icon}</span>
          </div>
        </div>
      )}
      {title && <h3 className="mb-3 text-xl font-bold text-alc-light-blue">{title}</h3>}
      {children}
    </div>
  );
}
