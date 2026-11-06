export class Codec {
  public callCount = 0;

  constructor(private readonly delimiter = ':') {}

  encode(strings: string[]): string {
    return strings.map((value) => `${value.length}${this.delimiter}${value}`).join('');
  }

  decode(encoded: string): string[] {
    const result: string[] = [];
    let index = 0;

    while (index < encoded.length) {
      const delimiterIndex = encoded.indexOf(this.delimiter, index);
      if (delimiterIndex === -1) {
        throw new Error('Invalid encoded string: missing length delimiter');
      }

      const length = Number(encoded.slice(index, delimiterIndex));
      if (!Number.isInteger(length) || length < 0) {
        throw new Error('Invalid encoded string: invalid length');
      }

      const valueStart = delimiterIndex + this.delimiter.length;
      const valueEnd = valueStart + length;
      if (valueEnd > encoded.length) {
        throw new Error('Invalid encoded string: incomplete value');
      }

      result.push(encoded.slice(valueStart, valueEnd));
      index = valueEnd;
    }

    return result;
  }

  static create(delimiter?: string): Codec {
    return new Codec(delimiter);
  }

  get separator(): string {
    return this.delimiter;
  }
}

export function encode(strings: string[]): string {
  return new Codec().encode(strings);
}

export function decode(encoded: string): string[] {
  return new Codec().decode(encoded);
}
