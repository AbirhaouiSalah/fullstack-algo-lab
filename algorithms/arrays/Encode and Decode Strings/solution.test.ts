import { describe, expect, test, beforeEach } from 'vitest';
import { 
    Codec, 
    // CodecStatic, 
    // createCodec,
    encode,
    decode
} from './solution';

describe('Encode and Decode Strings', () => {
    let codec: Codec;

    beforeEach(() => {
        codec = new Codec();
    });

    describe('Basic Functionality', () => {
        test('should encode and decode a list of strings', () => {
            const input = ['Hello', 'World'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle empty list', () => {
            const input: string[] = [];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle strings with empty strings', () => {
            const input = [''];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle multiple empty strings', () => {
            const input = ['', '', ''];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });
    });

    describe('Special Characters', () => {
        test('should handle strings with numbers', () => {
            const input = ['123', '456', '789'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle strings with special characters', () => {
            const input = ['Hello!', '@World#', '$%^&*()'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle strings with delimiter character (#)', () => {
            const input = ['Hello#World', 'Test#Case', 'No#Delimiter'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle strings with spaces', () => {
            const input = ['Hello World', '  leading', 'trailing  ', 'multiple   spaces'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle Unicode characters', () => {
            const input = ['Hello', '🌍', 'привет', '你好', '👨‍💻'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });
    });

    describe('Edge Cases', () => {
        test('should handle very long strings', () => {
            const longString = 'a'.repeat(10000);
            const input = [longString, 'short', longString];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle many strings', () => {
            const input = Array.from({ length: 1000 }, (_, i) => `string${i}`);
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle strings that look like lengths', () => {
            const input = ['5#Hello', '10#World', '42#Answer'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });

        test('should handle single character strings', () => {
            const input = ['a', 'b', 'c', 'd', 'e'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
        });
    });

    describe('Round Trip Tests', () => {
        test('should maintain order of strings', () => {
            const input = ['first', 'second', 'third', 'fourth'];
            const encoded = codec.encode(input);
            const decoded = codec.decode(encoded);
            expect(decoded).toEqual(input);
            expect(decoded[0]).toBe('first');
            expect(decoded[decoded.length - 1]).toBe('fourth');
        });

        test('should encode and decode multiple times without issues', () => {
            const input = ['test', 'multiple', 'round', 'trips'];
            let result = input;
            
            // Do 10 round trips
            for (let i = 0; i < 10; i++) {
                const encoded = codec.encode(result);
                result = codec.decode(encoded);
            }
            
            expect(result).toEqual(input);
        });

        // test('should handle nested encoding', () => {
        //     const inner = ['inner1', 'inner2'];
        //     const outer = ['outer', codec.encode(inner), 'end'];
        //     const encoded = codec.encode(outer);
        //     const decoded = codec.decode(encoded);
        //     expect(decoded).toEqual(outer);
        //     
        //     // Decode the inner string
        //     const innerDecoded = codec.decode(decoded[1]);
        //     expect(innerDecoded).toEqual(inner);
        // });
//    });

    // describe('Different Encodings', () => {
    //     test('should handle different approaches consistently', () => {
    //         const input = ['Hello', 'World', 'Test'];
            
    //         const encoded1 = codec.encode(input);
    //         const decoded1 = codec.decode(encoded1);
            
    //         const encoded2 = codec.encodeWithDelimiter(input);
    //         const decoded2 = codec.decodeWithDelimiter(encoded2);
            
    //         const encoded3 = codec.encodeChunked(input);
    //         const decoded3 = codec.decodeChunked(encoded3);
            
    //         expect(decoded1).toEqual(input);
    //         expect(decoded2).toEqual(input);
    //         expect(decoded3).toEqual(input);
    //     });

    //     test('should handle JSON encoding', () => {
    //         const input = ['Hello', 'World', 'With "quotes"', 'and \\backslashes'];
    //         const encoded = codec.encodeJSON(input);
    //         const decoded = codec.decodeJSON(encoded);
    //         expect(decoded).toEqual(input);
    //     });

    //     test('should handle escaped encoding', () => {
    //         const input = ['Hello:World', 'Test\\Case', 'Normal'];
    //         const encoded = codec.encodeEscaped(input);
    //         const decoded = codec.decodeEscaped(encoded);
    //         expect(decoded).toEqual(input);
    //     });

    //     test('should handle Base64 encoding', () => {
    //         const input = ['Hello', 'World', 'Test'];
    //         const encoded = codec.encodeBase64(input);
    //         const decoded = codec.decodeBase64(encoded);
    //         expect(decoded).toEqual(input);
    //     });
    // });

    // describe('Static Methods and Functional Approach', () => {
    //     test('should work with static methods', () => {
    //         const input = ['Hello', 'World'];
    //         const encoded = CodecStatic.encode(input);
    //         const decoded = CodecStatic.decode(encoded);
    //         expect(decoded).toEqual(input);
    //     });

    //     test('should work with factory function', () => {
    //         const c = createCodec();
    //         const input = ['Hello', 'World'];
    //         const encoded = c.encode(input);
    //         const decoded = c.decode(encoded);
    //         expect(decoded).toEqual(input);
    //     });

        test('should work with functional approach', () => {
            const input = ['Hello', 'World'];
            const encoded = encode(input);
            const decoded = decode(encoded);
            expect(decoded).toEqual(input);
        });
    });

    //describe('Error Cases', () => {
    //    test('should handle malformed encoded string gracefully', () => {
    //        const malformed = '5#Hello3#World';
    //        const decoded = codec.decode(malformed);
    //        expect(decoded).toEqual(['Hello', 'Wor']); // Should parse as much as possible
    //    });
//
    //    test('should handle empty string as input', () => {
    //        const encoded = codec.encode([]);
    //        expect(encoded).toBe('');
    //        const decoded = codec.decode('');
    //        expect(decoded).toEqual([]);
    //    });
    //});

    // describe('Performance', () => {
    //     test('should handle large input efficiently', () => {
    //         const largeInput = Array.from(
    //             { length: 1000 }, 
    //             (_, i) => 'string'.repeat(100) + i.toString()
    //         );
    //         
    //         const startEncode = performance.now();
    //         const encoded = codec.encode(largeInput);
    //         const encodeTime = performance.now() - startEncode;
    //         
    //         const startDecode = performance.now();
    //         const decoded = codec.decode(encoded);
    //         const decodeTime = performance.now() - startDecode;
    //         
    //         console.log(`Encode time: ${encodeTime.toFixed(2)}ms`);
    //         console.log(`Decode time: ${decodeTime.toFixed(2)}ms`);
    //         
    //         expect(decoded).toEqual(largeInput);
    //         expect(encodeTime).toBeLessThan(1000); // Should be fast
    //         expect(decodeTime).toBeLessThan(1000);
    //     });
    // });
});

describe('Integration Tests', () => {
    test('should simulate network transmission', () => {
        const codec = new Codec();
        
        // Machine 1 (Sender)
        const original = ['Hello', 'World', 'Encoding', 'Test'];
        const encoded = codec.encode(original);
        
        // Simulate network transmission (string over network)
        const transmitted = encoded;
        
        // Machine 2 (Receiver)
        const decoded = codec.decode(transmitted);
        
        expect(decoded).toEqual(original);
    });

    test('should handle real-world scenarios', () => {
        const codec = new Codec();
        
        // Simulate user messages
        const messages = [
            'Hello, how are you?',
            'I\'m fine, thank you!',
            'Check out this link: https://example.com',
            '😊🎉🎊',
            'Multiple lines\nwith\nnewlines',
            'Tab\tseparated\tvalues',
        ];
        
        const encoded = codec.encode(messages);
        const decoded = codec.decode(encoded);
        
        expect(decoded).toEqual(messages);
    });
});