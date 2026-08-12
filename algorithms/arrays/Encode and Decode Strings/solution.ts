/**
 * Encode and Decode Strings
 * 
 * Design an algorithm to encode a list of strings to a single string.
 * The encoded string is then decoded back to the original list of strings.
 * 
 * Approach: Length-prefix encoding with delimiter
 * Format: [length]#[string][length]#[string]...
 * Example: ["Hello", "World"] -> "5#Hello5#World"
 */

/**
 * Solution class with encode and decode methods
 */
export class Codec {
    /**
     * Encodes a list of strings to a single string.
     * 
     * Approach 1: Length-prefix with '#' delimiter (Recommended)
     * Time: O(m) where m is sum of lengths of all strings
     * Space: O(m + n) for the encoded string
     * 
     * @param strs - List of strings to encode
     * @returns Encoded string
     */
    encode(strs: string[]): string {
        let encoded = '';
        
        for (const str of strs) {
            // Prepend length and '#' delimiter before each string
            encoded += str.length + '#' + str;
        }
        
        return encoded;
    }

    /**
     * Decodes a single string back to a list of strings.
     * 
     * Time: O(m) where m is sum of lengths of all strings
     * Space: O(m + n) for the decoded list
     * 
     * @param s - Encoded string
     * @returns Decoded list of strings
     */
    decode(s: string): string[] {
        const result: string[] = [];
        let i = 0;
        
        while (i < s.length) {
            // Find the position of the next '#'
            let j = i;
            while (j < s.length && s[j] !== '#') {
                j++;
            }
            
            // Parse the length (number before '#')
            const length = parseInt(s.substring(i, j));
            
            // Skip the '#'
            j++;
            
            // Extract the string of the specified length
            const str = s.substring(j, j + length);
            result.push(str);
            
            // Move to the next string
            i = j + length;
        }
        
        return result;
    }

    /**
     * Approach 2: Using non-ASCII delimiter (Simpler but less robust)
     * Uses a Unicode character that won't appear in input
     * 
     * Time: O(m) | Space: O(m + n)
     */
    encodeWithDelimiter(strs: string[]): string {
        // Using Unicode character that's unlikely to appear in input
        const delimiter = String.fromCharCode(257); // 'ā'
        return strs.join(delimiter);
    }

    decodeWithDelimiter(s: string): string[] {
        const delimiter = String.fromCharCode(257); // 'ā'
        return s.split(delimiter);
    }

    /**
     * Approach 3: Chunk-based encoding with 4-byte length prefix
     * More robust for binary data
     * 
     * Time: O(m) | Space: O(m + n)
     */
    encodeChunked(strs: string[]): string {
        const result: string[] = [];
        
        for (const str of strs) {
            // Convert length to 4-byte hexadecimal
            const lengthHex = str.length.toString(16).padStart(8, '0');
            result.push(lengthHex + str);
        }
        
        return result.join('');
    }

    decodeChunked(s: string): string[] {
        const result: string[] = [];
        let i = 0;
        
        while (i < s.length) {
            // Read 8 characters for the length
            const lengthHex = s.substring(i, i + 8);
            const length = parseInt(lengthHex, 16);
            i += 8;
            
            // Extract the string of the specified length
            const str = s.substring(i, i + length);
            result.push(str);
            i += length;
        }
        
        return result;
    }

    /**
     * Approach 4: JSON-based encoding (Simple but with overhead)
     * 
     * Time: O(m) | Space: O(m + n)
     */
    encodeJSON(strs: string[]): string {
        return JSON.stringify(strs);
    }

    decodeJSON(s: string): string[] {
        return JSON.parse(s);
    }

    /**
     * Approach 5: Length-prefix with escaping (Handles any characters)
     * Uses ':' as delimiter and '\\' as escape character
     * 
     * Time: O(m) | Space: O(m + n)
     */
    encodeEscaped(strs: string[]): string {
        const escaped = strs.map(str => {
            // Escape ':' and '\\' characters
            return str.replace(/\\/g, '\\\\').replace(/:/g, '\\:');
        });
        return escaped.join(':');
    }

    decodeEscaped(s: string): string[] {
        const result: string[] = [];
        let current = '';
        let i = 0;
        
        while (i < s.length) {
            if (s[i] === '\\') {
                // Skip escape character and take the next character as is
                current += s[i + 1];
                i += 2;
            } else if (s[i] === ':') {
                // Delimiter found
                result.push(current);
                current = '';
                i++;
            } else {
                current += s[i];
                i++;
            }
        }
        
        // Add the last string
        result.push(current);
        return result;
    }

    /**
     * Approach 6: Base64 encoding for binary-safe transmission
     * 
     * Time: O(m) | Space: O(m + n)
     */
    encodeBase64(strs: string[]): string {
        // First encode using length-prefix, then base64
        const encoded = this.encode(strs);
        return btoa(encoded);
    }

    decodeBase64(s: string): string[] {
        const decoded = atob(s);
        return this.decode(decoded);
    }
}

/**
 * Alternative: Using a class with static methods
 */
export class CodecStatic {
    static encode(strs: string[]): string {
        return strs.map(str => `${str.length}#${str}`).join('');
    }

    static decode(s: string): string[] {
        const result: string[] = [];
        let i = 0;
        
        while (i < s.length) {
            let j = i;
            while (j < s.length && s[j] !== '#') j++;
            const length = parseInt(s.substring(i, j));
            j++;
            result.push(s.substring(j, j + length));
            i = j + length;
        }
        
        return result;
    }
}

/**
 * Factory function for creating codec instances
 */
export function createCodec(): Codec {
    return new Codec();
}

/**
 * Functional approach
 */
export const encode = (strs: string[]): string => {
    return strs.map(str => `${str.length}#${str}`).join('');
};

export const decode = (s: string): string[] => {
    const result: string[] = [];
    let i = 0;
    
    while (i < s.length) {
        let j = i;
        while (j < s.length && s[j] !== '#') j++;
        const length = parseInt(s.substring(i, j));
        j++;
        result.push(s.substring(j, j + length));
        i = j + length;
    }
    
    return result;
};