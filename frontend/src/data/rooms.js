// export const rooms = [
//   {
//     id: 1,
//     name: "Piscine meeting room",
//     //seats: 10,
//     color:
//       "bg-blue-50 border-blue-200 text-blue-600",
//     accent: "#3B82F6",
//   },

//   {
//     id: 2,
//     name: "Galaxy meeting room",
//     //seats: 8,
//     color:
//       "bg-emerald-50 border-emerald-200 text-emerald-600",
//     accent: "#10B981",
//   },

//   {
//     id: 3,
//     name: "Space invaders meeting room",
//     //seats: 12,
//     color:
//       "bg-violet-50 border-violet-200 text-violet-600",
//     accent: "#8B5CF6",
//   },

//   {
//     id: 4,
//     name: "Gallery meeting room",
//     //seats: 4,
//     color:
//       "bg-orange-50 border-orange-200 text-orange-500",
//     accent: "#F97316",
//   },
// ];

export const rooms = [
  { id: 1, name: "Piscine meeting room", slug: "piscine"},
  { id: 2, name: "Galaxy meeting room", slug: "galaxy"},
  { id: 3, name: "Space invaders meeting room", slug: "space-invader"},
  { id: 4, name: "Gallery meeting room", slug: "gallery"},
];

export const eventsData = {
  1: [
    {
      title: "Client Call",
      start: new Date(2025, 4, 12, 10, 0),
      end: new Date(2025, 4, 12, 11, 0),
    },
  ],

  2: [
    {
      title: "Product Sync",
      start: new Date(2025, 4, 13, 11, 0),
      end: new Date(2025, 4, 13, 12, 30),
    },
  ],

  3: [
    {
      title: "Weekly Team Sync",
      start: new Date(2025, 4, 12, 9, 0),
      end: new Date(2025, 4, 12, 10, 30),
    },

    {
      title: "Client Presentation",
      start: new Date(2025, 4, 12, 11, 0),
      end: new Date(2025, 4, 12, 12, 30),
    },

    {
      title: "Design Thinking",
      start: new Date(2025, 4, 14, 9, 30),
      end: new Date(2025, 4, 14, 11, 0),
    },

    {
      title: "Workshop: Ideation",
      start: new Date(2025, 4, 14, 12, 0),
      end: new Date(2025, 4, 14, 14, 0),
    },

    {
      title: "Interview",
      start: new Date(2025, 4, 16, 10, 0),
      end: new Date(2025, 4, 16, 11, 0),
    },

    {
      title: "Sprint Planning",
      start: new Date(2025, 4, 16, 16, 0),
      end: new Date(2025, 4, 16, 17, 30),
    },

    {
      title: "Stakeholder Review",
      start: new Date(2025, 4, 12, 16, 0),
      end: new Date(2025, 4, 12, 17, 0),
    },
  ],

  4: [
    {
      title: "Creative Review",
      start: new Date(2025, 4, 15, 13, 0),
      end: new Date(2025, 4, 15, 14, 0),
    },
  ],
};