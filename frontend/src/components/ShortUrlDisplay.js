import React from "react";

export default function ShortUrlDisplay({ shortUrl }) {
  if (!shortUrl) return null;

  return (
    <p style={styles.result}>
      Short URL: <a href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a>
    </p>
  );
}

const styles = {
  result: {
    marginTop: "1rem",
    fontSize: "1.2rem"
  }
};
