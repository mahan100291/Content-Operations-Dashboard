import type { NextApiRequest, NextApiResponse } from 'next';
import { channelMetrics, workflowStages } from '@/data/contentMetrics';

export default function handler(_request: NextApiRequest, response: NextApiResponse) {
  response.status(200).json({
    channels: channelMetrics,
    workflow: workflowStages,
  });
}
