export function Navigation({ tabs, activeTab, onTabChange }) {
  return (
    <nav className="w-full border-b border-alc-purple/20 bg-alc-navy">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <div className="flex gap-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`border-b-2 px-4 py-4 font-semibold transition-all duration-300 ${
                activeTab === tab.id
                  ? 'border-alc-cyan text-alc-light-blue'
                  : 'border-transparent text-gray-400 hover:text-alc-cyan'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}
