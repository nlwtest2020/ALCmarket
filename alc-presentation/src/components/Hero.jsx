import { Button } from './Button';

export function Hero({
  title,
  subtitle,
  description,
  buttons = [],
  image,
}) {
  return (
    <section className="relative w-full bg-gradient-to-b from-alc-navy to-alc-dark px-4 py-20 sm:px-6 lg:px-8">
      {/* Accent line */}
      <div className="absolute left-0 top-1/4 h-1 w-32 bg-gradient-to-r from-alc-magenta to-alc-cyan"></div>

      <div className="mx-auto max-w-6xl">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          {/* Left content */}
          <div className="space-y-6">
            {title && <h1 className="text-4xl font-bold sm:text-5xl">{title}</h1>}
            {subtitle && <h2 className="text-2xl font-semibold text-alc-light-blue">{subtitle}</h2>}
            {description && <p className="text-lg text-gray-300">{description}</p>}

            {/* Buttons */}
            {buttons.length > 0 && (
              <div className="flex flex-wrap gap-4 pt-4">
                {buttons.map((btn, idx) => (
                  <Button
                    key={idx}
                    variant={btn.variant || 'primary'}
                    size={btn.size || 'md'}
                    onClick={btn.onClick}
                  >
                    {btn.label}
                  </Button>
                ))}
              </div>
            )}
          </div>

          {/* Right image/content */}
          {image && (
            <div className="flex items-center justify-center">
              <img src={image} alt="Hero" className="max-w-full rounded-lg" />
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
