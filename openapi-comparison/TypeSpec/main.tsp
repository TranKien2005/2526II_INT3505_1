import "@typespec/http";

using TypeSpec.Http;

@service(#{
  title: "Library Management API",
})
namespace LibraryApi;

model Book {
  id: string;
  title: string;
  author: string;
  year: int32;
}

model BookInput {
  title: string;
  author: string;
  year: int32;
}

@route("/books")
interface Books {
  @get list(): Book[];
  
  @post create(@body book: BookInput): Book;
  
  @route("/{id}")
  @get read(@path id: string): Book;

  @route("/{id}")
  @delete delete_(@path id: string): void;
}
