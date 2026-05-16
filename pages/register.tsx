import Head from 'next/head';
import Link from 'next/link';
import { useState, type FormEvent } from 'react';
import { motion } from 'motion/react';
import styles from '@/styles/Register.module.css';

type RegistrationForm = {
  fullName: string;
  email: string;
  phone: string;
  role: string;
  organization: string;
  contentFocus: string;
  notes: string;
  acceptedTerms: boolean;
};

const initialForm: RegistrationForm = {
  fullName: '',
  email: '',
  phone: '',
  role: '',
  organization: '',
  contentFocus: 'Social publishing',
  notes: '',
  acceptedTerms: false,
};

export default function Register() {
  const [form, setForm] = useState<RegistrationForm>(initialForm);
  const [submittedName, setSubmittedName] = useState('');

  function updateField<K extends keyof RegistrationForm>(field: K, value: RegistrationForm[K]) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmittedName(form.fullName);
    setForm(initialForm);
  }

  return (
    <>
      <Head>
        <title>Individual Registration | Content Operations Dashboard</title>
        <meta
          name="description"
          content="Register an individual contributor for the content operations dashboard."
        />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>

      <main className={styles.page}>
        <motion.section
          className={styles.header}
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.38, ease: 'easeOut' }}
        >
          <Link className={styles.backLink} href="/">
            Back to dashboard
          </Link>
          <span className={styles.eyebrow}>Individual registration</span>
          <h1>Create a contributor profile for content operations.</h1>
          <p>
            Capture contact details, team context, and content focus so an individual can be
            onboarded into the publishing workflow.
          </p>
        </motion.section>

        <section className={styles.layout}>
          <motion.form
            className={styles.form}
            onSubmit={handleSubmit}
            initial={{ opacity: 0, y: 14 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.38, delay: 0.08, ease: 'easeOut' }}
          >
            <div className={styles.fieldGroup}>
              <label htmlFor="fullName">Full name</label>
              <input
                id="fullName"
                name="fullName"
                type="text"
                autoComplete="name"
                value={form.fullName}
                onChange={(event) => updateField('fullName', event.target.value)}
                required
              />
            </div>

            <div className={styles.twoColumn}>
              <div className={styles.fieldGroup}>
                <label htmlFor="email">Email address</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  value={form.email}
                  onChange={(event) => updateField('email', event.target.value)}
                  required
                />
              </div>

              <div className={styles.fieldGroup}>
                <label htmlFor="phone">Phone number</label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  autoComplete="tel"
                  value={form.phone}
                  onChange={(event) => updateField('phone', event.target.value)}
                />
              </div>
            </div>

            <div className={styles.twoColumn}>
              <div className={styles.fieldGroup}>
                <label htmlFor="role">Role</label>
                <select
                  id="role"
                  name="role"
                  value={form.role}
                  onChange={(event) => updateField('role', event.target.value)}
                  required
                >
                  <option value="">Select role</option>
                  <option value="Content manager">Content manager</option>
                  <option value="Creator">Creator</option>
                  <option value="Approver">Approver</option>
                  <option value="Analyst">Analyst</option>
                </select>
              </div>

              <div className={styles.fieldGroup}>
                <label htmlFor="organization">Organization</label>
                <input
                  id="organization"
                  name="organization"
                  type="text"
                  autoComplete="organization"
                  value={form.organization}
                  onChange={(event) => updateField('organization', event.target.value)}
                  required
                />
              </div>
            </div>

            <fieldset className={styles.radioGroup}>
              <legend>Primary content focus</legend>
              {['Social publishing', 'Campaign planning', 'Editorial approvals'].map((focus) => (
                <label key={focus}>
                  <input
                    type="radio"
                    name="contentFocus"
                    value={focus}
                    checked={form.contentFocus === focus}
                    onChange={(event) => updateField('contentFocus', event.target.value)}
                  />
                  <span>{focus}</span>
                </label>
              ))}
            </fieldset>

            <div className={styles.fieldGroup}>
              <label htmlFor="notes">Notes</label>
              <textarea
                id="notes"
                name="notes"
                rows={4}
                value={form.notes}
                onChange={(event) => updateField('notes', event.target.value)}
                placeholder="Add onboarding context, permissions, or preferred channels."
              />
            </div>

            <label className={styles.checkbox} htmlFor="workspaceConsent">
              <input
                id="workspaceConsent"
                type="checkbox"
                checked={form.acceptedTerms}
                onChange={(event) => updateField('acceptedTerms', event.target.checked)}
                required
              />
              <span>I confirm this individual can be added to the content workspace.</span>
            </label>

            <button className={styles.submitButton} type="submit">
              Submit registration
            </button>

            {submittedName ? (
              <p className={styles.success} role="status">
                Registration captured for {submittedName}.
              </p>
            ) : null}
          </motion.form>

          <aside className={styles.sidePanel} aria-label="Registration summary">
            <h2>Profile details collected</h2>
            <ul>
              <li>Identity and contact information</li>
              <li>Role and organization context</li>
              <li>Primary content workflow focus</li>
              <li>Optional onboarding notes</li>
            </ul>
          </aside>
        </section>
      </main>
    </>
  );
}
