(function bootstrapCoursePdfRenderer() {
  "use strict";

  var READY_FLAG = "__COURSE_PDF_READY__";
  var contentRoot = document.getElementById("pdf-course-content") || document.body;

  var tagClassMap = {
    h1: "pdf-h1",
    h2: "pdf-h2",
    h3: "pdf-h3",
    h4: "pdf-h4",
    h5: "pdf-h5",
    h6: "pdf-h6",
    p: "pdf-p",
    ul: "pdf-list",
    ol: "pdf-list",
    li: "pdf-li",
    table: "pdf-table",
    pre: "pdf-code",
    img: "pdf-image",
    blockquote: "pdf-quote"
  };

  function stripWhitespace(value) {
    return (value || "").toLowerCase().replace(/\s+/g, "");
  }

  function addClassFromStyle(node, compactStyle, tagName) {
    if (!compactStyle) {
      return;
    }

    if (
      compactStyle.indexOf("border:1pxsolid#e1e8ed") >= 0 ||
      compactStyle.indexOf("border:1pxsolid#dbe4ee") >= 0
    ) {
      node.classList.add("pdf-section-card");
    }

    if (
      compactStyle.indexOf("background:#e8f4fd") >= 0 ||
      compactStyle.indexOf("border-left:6pxsolid#3498db") >= 0
    ) {
      node.classList.add("pdf-callout", "pdf-callout--info");
    }

    if (
      compactStyle.indexOf("background:#ecfdf5") >= 0 ||
      compactStyle.indexOf("#10b981") >= 0
    ) {
      node.classList.add("pdf-callout", "pdf-callout--success");
    }

    if (
      compactStyle.indexOf("background:#fef3c7") >= 0 ||
      compactStyle.indexOf("#f59e0b") >= 0
    ) {
      node.classList.add("pdf-callout", "pdf-callout--warning");
    }

    if (
      compactStyle.indexOf("background:#fee2e2") >= 0 ||
      compactStyle.indexOf("#dc2626") >= 0
    ) {
      node.classList.add("pdf-callout", "pdf-callout--danger");
    }

    if (tagName === "pre" && compactStyle.indexOf("background:#2d2d2d") >= 0) {
      node.classList.add("pdf-code", "pdf-code--dark");
    }

    if (tagName === "table" || compactStyle.indexOf("border-collapse:collapse") >= 0) {
      node.classList.add("pdf-table");
    }

    if (
      (tagName === "tr" || tagName === "th" || tagName === "td") &&
      compactStyle.indexOf("background:#3498db") >= 0
    ) {
      node.classList.add("pdf-table-row--head");
    }

    if (
      (tagName === "tr" || tagName === "th" || tagName === "td") &&
      compactStyle.indexOf("background:#f8f9fa") >= 0
    ) {
      node.classList.add("pdf-table-row--alt");
    }
  }

  function sanitizeAttributes(node) {
    if (!node.attributes || !node.attributes.length) {
      return;
    }

    var namesToDelete = [];

    for (var i = 0; i < node.attributes.length; i += 1) {
      var attr = node.attributes[i];
      var attrName = attr.name.toLowerCase();
      var attrValue = (attr.value || "").trim();

      if (attrName.indexOf("on") === 0) {
        namesToDelete.push(attr.name);
        continue;
      }

      if (
        (attrName === "href" || attrName === "src") &&
        /^javascript:/i.test(attrValue)
      ) {
        namesToDelete.push(attr.name);
      }
    }

    for (var j = 0; j < namesToDelete.length; j += 1) {
      node.removeAttribute(namesToDelete[j]);
    }
  }

  function normalizeNode(node) {
    if (!node || !node.tagName) {
      return;
    }

    sanitizeAttributes(node);

    var tagName = node.tagName.toLowerCase();
    if (tagClassMap[tagName]) {
      node.classList.add(tagClassMap[tagName]);
    }

    var rawStyle = node.getAttribute("style");
    var compactStyle = stripWhitespace(rawStyle);
    addClassFromStyle(node, compactStyle, tagName);

    if (node.hasAttribute("style")) {
      node.removeAttribute("style");
    }
  }

  function normalizeDocument() {
    contentRoot.classList.add("pdf-content-root");
    normalizeNode(contentRoot);

    var allNodes = contentRoot.querySelectorAll("*");
    for (var i = 0; i < allNodes.length; i += 1) {
      normalizeNode(allNodes[i]);
    }
  }

  function renderMathIfAvailable() {
    if (typeof window.renderMathInElement !== "function") {
      return false;
    }

    try {
      window.renderMathInElement(contentRoot, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "$", right: "$", display: false },
          { left: "\\(", right: "\\)", display: false }
        ],
        throwOnError: false,
        strict: "ignore",
        ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
      });
    } catch (error) {
      console.warn("KaTeX auto-render failed:", error);
    }

    return true;
  }

  function markReady() {
    window[READY_FLAG] = true;
    document.documentElement.classList.add("pdf-ready");
  }

  function boot() {
    normalizeDocument();

    var deadline = Date.now() + 8000;
    (function waitForMath() {
      if (renderMathIfAvailable()) {
        markReady();
        return;
      }
      if (Date.now() >= deadline) {
        markReady();
        return;
      }
      setTimeout(waitForMath, 120);
    })();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot, { once: true });
  } else {
    boot();
  }
})();
