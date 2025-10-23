import React from "react";
import { commonStyles } from "../styles/commonStyles";

export default function ShortUrlDisplay({ shortUrl }) {
  if (!shortUrl) return null;

  return (
    <p style={commonStyles.url_result}>
      Short URL: <a href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a>
    </p>
  );
}
