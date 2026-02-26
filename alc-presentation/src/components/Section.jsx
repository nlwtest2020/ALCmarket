export function Section({
  title,
  subtitle,
  children,
  className = '',
  withAccentLine = false,
}) {
  return (
    <section className={`relative w-full bg-alc-dark px-4 py-16 sm:px-6 lg:px-8 ${className}`}>
      {withAccentLine && (
        <div className="absolute left-0 top-12 h-1 w-32 bg-gradient-to-r from-alc-magenta to-alc-cyan"></div>
      )}

      <div className="mx-auto max-w-6xl">
        {title && (
          <div className="mb-12">
            <h2 className="mb-2 text-3xl font-bold text-alc-light-blue sm:text-4xl">{title}</h2>
            {subtitle && <p className="text-lg text-gray-400">{subtitle}</p>}
          </div>
        )}

        {children}
      </div>
    </section>
  );
}
