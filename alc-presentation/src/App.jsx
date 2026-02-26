import { useState } from 'react';
import { Button, Card, Hero, Navigation, Section } from './components';

function App() {
  const [activeTab, setActiveTab] = useState('overview');

  const navigationTabs = [
    { id: 'overview', label: 'View Objectives' },
    { id: 'timeline', label: 'See Timeline' },
    { id: 'outcomes', label: 'View Outcomes' },
  ];

  const features = [
    {
      icon: '🎯',
      title: 'Strategic Focus',
      description: 'Align your goals with market opportunities and customer needs.',
    },
    {
      icon: '📈',
      title: 'Growth Metrics',
      description: 'Track progress with data-driven insights and performance indicators.',
    },
    {
      icon: '🚀',
      title: 'Market Launch',
      description: 'Execute campaigns with precision and competitive positioning.',
    },
    {
      icon: '💡',
      title: 'Innovation Path',
      description: 'Identify emerging opportunities and market gaps.',
    },
  ];

  return (
    <div className="w-full bg-alc-dark">
      {/* Hero Section */}
      <Hero
        title="6-Month Strategic Overview"
        subtitle="Accelerate Your Growth"
        description="Data-driven positioning for academic and skill-based learning courses in Eastern European markets."
        buttons={[
          { label: 'Get Started', variant: 'primary', size: 'lg' },
          { label: 'Learn More', variant: 'secondary', size: 'lg' },
        ]}
      />

      {/* Navigation Tabs */}
      <Navigation tabs={navigationTabs} activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Content Section */}
      <Section
        title="Key Initiatives"
        subtitle="Strategic pillars for the next 6 months"
        withAccentLine
        className="bg-gradient-to-b from-alc-dark to-alc-navy"
      >
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {features.map((feature, idx) => (
            <Card
              key={idx}
              icon={feature.icon}
              title={feature.title}
              hoverable
              className="h-full"
            >
              <p className="text-gray-400">{feature.description}</p>
            </Card>
          ))}
        </div>
      </Section>

      {/* CTA Section */}
      <Section
        title="Ready to Transform Your Course Offering?"
        subtitle="Join leading institutions across Moldova, Georgia, and Armenia"
        className="bg-alc-dark"
      >
        <div className="flex flex-col items-center gap-8 sm:flex-row sm:justify-center">
          <Button variant="primary" size="lg">
            Schedule Consultation
          </Button>
          <Button variant="outline" size="lg">
            View Case Studies
          </Button>
        </div>
      </Section>

      {/* Footer Section */}
      <Section className="border-t border-alc-purple/20 bg-alc-navy py-8">
        <div className="text-center">
          <p className="text-gray-500">
            © 2026 ALC Presentation. All rights reserved.
          </p>
        </div>
      </Section>
    </div>
  );
}

export default App;
