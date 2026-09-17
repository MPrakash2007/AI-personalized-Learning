import React from 'react';
import TopicNode from './TopicNode';

export default function VisualLearningPath({ topics, subjectSlug }) {
  if (!topics || topics.length === 0) {
    return (
      <div className="text-center py-12 text-slate-400">
        No topics configured for this curriculum yet.
      </div>
    );
  }

  return (
    <div className="relative py-8 px-4 flex flex-col items-center">
      {/* Background Central Glow Line */}
      <div className="absolute top-12 bottom-12 w-1.5 bg-gradient-to-b from-cyan-500/40 via-purple-500/40 to-amber-500/40 rounded-full blur-[1px]" />

      <div className="w-full max-w-md space-y-6 relative z-10">
        {topics.map((topic, index) => {
          // Subtle horizontal alternating stagger for winding feel on desktop
          const offsetClass =
            index % 3 === 0
              ? 'translate-x-0'
              : index % 3 === 1
              ? 'sm:translate-x-12'
              : 'sm:-translate-x-12';

          return (
            <div
              key={topic.id}
              className={`flex justify-center transition-transform duration-300 ${offsetClass}`}
            >
              <TopicNode
                topic={topic}
                subjectSlug={subjectSlug}
                isBoss={topic.is_boss}
                index={index}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
}
