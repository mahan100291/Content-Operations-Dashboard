declare module '*.css' {
  const content: string;
  export default content;
}

declare module '*.module.css' {
  const content: { [className: string]: string };
  export default content;
}

declare module '@/styles/Home.module.css' {
  const content: { [className: string]: string };
  export default content;
}

declare module '@/styles/globals.css' {
  const content: string;
  export default content;
}
