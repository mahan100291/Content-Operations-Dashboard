import Head from 'next/head';
import dynamic from 'next/dynamic';
import Link from 'next/link';
import * as Tabs from '@radix-ui/react-tabs';
import { Popover } from '@base-ui/react/popover';
import { motion } from 'motion/react';
import { channelMetrics, workflowStages } from '@/data/contentMetrics';
import styles from '@/styles/Home.module.css';

const ResponsiveContainer = dynamic(
  () => import('recharts').then((module) => module.ResponsiveContainer),
  { ssr: false },
);
const BarChart = dynamic(() => import('recharts').then((module) => module.BarChart), { ssr: false });
const Bar = dynamic(() => import('recharts').then((module) => module.Bar), { ssr: false });
const XAxis = dynamic(() => import('recharts').then((module) => module.XAxis), { ssr: false });
const YAxis = dynamic(() => import('recharts').then((module) => module.YAxis), { ssr: false });
const Tooltip = dynamic(() => import('recharts').then((module) => module.Tooltip), { ssr: false });
const CartesianGrid = dynamic(
  () => import('recharts').then((module) => module.CartesianGrid),
  { ssr: false },
);

export default function Home() {
  const totalScheduled = channelMetrics.reduce((total, item) => total + item.scheduled, 0);
  const totalPublished = channelMetrics.reduce((total, item) => total + item.published, 0);
  const averageEngagement = Math.round(
    channelMetrics.reduce((total, item) => total + item.engagement, 0) / channelMetrics.length,
  );

  return (
    <>
      <Head>
        <title>Social Content Dashboard</title>
        <meta
          name="description"
          content="Mini Next.js Pages Router dashboard using CSS Modules, Motion, Radix UI, Base UI, Next.js middleware, and Recharts."
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className={styles.page}>
        <section className={styles.hero}>
          <motion.div
            className={styles.heroCopy}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, ease: 'easeOut' }}
          >
            <span className={styles.eyebrow}>Content publishing operations</span>
            <h1>Plan, approve, and measure social posts from one focused workspace.</h1>
            <p>
              A small production-shaped dashboard for the stack: Pages Router today, native
              middleware routing, accessible primitives, CSS Modules, Motion, and Recharts.
            </p>
            <Link className={styles.heroAction} href="/register">
              Register an individual
            </Link>
          </motion.div>

          <motion.div
            className={styles.summaryGrid}
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.45, delay: 0.12, ease: 'easeOut' }}
          >
            <MetricCard label="Scheduled" value={totalScheduled} detail="Posts queued" />
            <MetricCard label="Published" value={totalPublished} detail="Posts shipped" />
            <MetricCard label="Engagement" value={`${averageEngagement}%`} detail="Avg. channel score" />
          </motion.div>
        </section>

        <Tabs.Root className={styles.workspace} defaultValue="overview">
          <Tabs.List className={styles.tabList} aria-label="Publishing dashboard views">
            <Tabs.Trigger className={styles.tabTrigger} value="overview">
              Overview
            </Tabs.Trigger>
            <Tabs.Trigger className={styles.tabTrigger} value="workflow">
              Workflow
            </Tabs.Trigger>
            <Tabs.Trigger className={styles.tabTrigger} value="routing">
              Routing
            </Tabs.Trigger>
          </Tabs.List>

          <Tabs.Content className={styles.tabPanel} value="overview">
            <section className={styles.chartSection}>
              <div>
                <h2>Channel output</h2>
                <p>Scheduled and published posts by channel for the current campaign window.</p>
              </div>
              <div className={styles.chartFrame}>
                <ResponsiveContainer width="100%" height={320}>
                  <BarChart data={channelMetrics} margin={{ top: 12, right: 12, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#dbe3ea" />
                    <XAxis dataKey="channel" tickLine={false} axisLine={false} />
                    <YAxis tickLine={false} axisLine={false} />
                    <Tooltip cursor={{ fill: 'rgba(44, 92, 99, 0.08)' }} />
                    <Bar dataKey="scheduled" fill="#2c5c63" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="published" fill="#f0b84f" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </section>
          </Tabs.Content>

          <Tabs.Content className={styles.tabPanel} value="workflow">
            <section className={styles.workflowGrid}>
              {workflowStages.map((stage, index) => (
                <motion.article
                  className={styles.workflowCard}
                  key={stage.label}
                  initial={{ opacity: 0, y: 12 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.35, delay: index * 0.08 }}
                >
                  <span>{String(index + 1).padStart(2, '0')}</span>
                  <h2>{stage.value}</h2>
                  <p>{stage.label}</p>
                </motion.article>
              ))}
            </section>
          </Tabs.Content>

          <Tabs.Content className={styles.tabPanel} value="routing">
            <section className={styles.routingPanel}>
              <div>
                <h2>Middleware migration sketch</h2>
                <p>
                  Native <code>middleware.ts</code> handles <code>/go/:workspace</code>, rewrites it
                  to the dashboard, and keeps the workspace context available without a custom
                  Express server.
                </p>
              </div>
              <Popover.Root>
                <Popover.Trigger className={styles.popoverButton}>View route behavior</Popover.Trigger>
                <Popover.Portal>
                  <Popover.Positioner sideOffset={8}>
                    <Popover.Popup className={styles.popover}>
                      <Popover.Arrow className={styles.popoverArrow} />
                      <h3>Example</h3>
                      <p>
                        Run <code>npm run dev</code> and visit <code>/go/team-growth</code>. Next.js
                        middleware renders the dashboard with a workspace query param.
                      </p>
                    </Popover.Popup>
                  </Popover.Positioner>
                </Popover.Portal>
              </Popover.Root>
            </section>
          </Tabs.Content>
        </Tabs.Root>
      </main>
    </>
  );
}

function MetricCard({ label, value, detail }: { label: string; value: number | string; detail: string }) {
  return (
    <article className={styles.metricCard}>
      <span>{label}</span>
      <strong>{value}</strong>
      <p>{detail}</p>
    </article>
  );
}
