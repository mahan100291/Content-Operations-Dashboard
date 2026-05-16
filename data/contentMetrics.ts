export type ChannelMetric = {
  channel: string;
  scheduled: number;
  published: number;
  engagement: number;
};

export const channelMetrics: ChannelMetric[] = [
  { channel: 'LinkedIn', scheduled: 42, published: 38, engagement: 78 },
  { channel: 'Instagram', scheduled: 35, published: 31, engagement: 84 },
  { channel: 'Threads', scheduled: 24, published: 21, engagement: 67 },
  { channel: 'TikTok', scheduled: 18, published: 15, engagement: 73 },
  { channel: 'X', scheduled: 31, published: 29, engagement: 58 },
];

export const workflowStages = [
  { label: 'Drafts reviewed', value: 124 },
  { label: 'Posts scheduled', value: 96 },
  { label: 'Approvals cleared', value: 87 },
];
