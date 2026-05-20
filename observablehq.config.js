export default {
  title: "Wurm Market Observatory",
  pages: [
    {
      name: "ARCHIVE LENSES",
      pages: [
        { name: "Seller Activity", path: "/lenses/seller" },
        { name: "Buyer Activity",  path: "/lenses/buyer" },
      ]
    },
    {
      name: "RESEARCH",
      pages: [
        { name: "Corpus Explorer", path: "/corpus" },
        { name: "Methodology",     path: "/methodology" },
      ]
    }
  ],
  footer: 'Wurm Market Observatory — derived data. Not canonical. Source: <a href="https://github.com/Jotasiete7/wurm-archive" target="_blank">Historical Archive</a>.',
  style: "style/observatory.css",
  toc: false,
  head: '<link rel="icon" href="/favicon.png" type="image/png">',
};

