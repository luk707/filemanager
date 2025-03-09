import { expect, test } from "vitest";
import { FILE_ICONS } from "./file-icon";
import mimeDB from "mime-db";

console.log(Object.keys(mimeDB));

test.for(Object.keys(mimeDB))(
  "Icon associated with contentType '%s'",
  (contentType) => {
    expect(contentType in FILE_ICONS).toBe(true);
  }
);
