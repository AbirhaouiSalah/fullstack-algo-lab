/**
 * debug.ts
 * ---------------------------------------------------------------------------
 * Trace pas à pas de tes deux implémentations de decode() SANS RIEN CORRIGER.
 * Le but est d'observer exactement où les valeurs divergent de ce qui est
 * attendu, avec un garde-fou anti-boucle-infinie pour rester exécutable.
 *
 * Usage : tsx debug.ts
 * ---------------------------------------------------------------------------
 */

const MAX_ITERATIONS = 20; // garde-fou : au-delà, on considère que c'est une boucle infinie

function separator(title: string): void {
    console.log('\n' + '='.repeat(70));
    console.log(title);
    console.log('='.repeat(70));
}

export class Codec {
    // --- Fields (typed, optionally with access modifiers) ---
    private delimiter: string;
    public callCount: number = 0;

    // --- Constructor ---
    constructor(delimiter: string = ':') {
        this.delimiter = delimiter;
    }

    // --- Regular instance method ---
    encode(strs: string[]): string {
        let encodedString: string = "";
        for (const s of strs) {
            if (s.includes(':')) {
                throw new Error("Input strings cannot contain the delimiter ':'");
            } else if (s.includes('#')) {
                throw new Error("Input strings cannot contain the delimiter '#'");
            } else if (s.length > 1000) {
                throw new Error("Input strings cannot exceed 1000 characters in length");
            } else if (s.length === 0) {
                throw new Error("Input strings cannot be empty");
            } else if (s.length < 1) {
                throw new Error("Input strings must have at least 1 character");
            } else {
                encodedString += `${s.length}:${s}`;
            }
        }
        return encodedString;
    }

    // --- Another instance method ---
    decode(s: string): string[] {
        separator(`Codec.decode("${s}")`);

        let decodedStrings: string[] = [];
        let current_index = 0;
        let current_lentgh = 0;
        let last_index = 0;

        const firstColon = s.indexOf(":", 0);
        current_index = s.indexOf(":", 0);
        current_lentgh = parseInt(s.substring(0, firstColon));
        console.log(
            `[init] firstColon=${firstColon}, ` +
            `current_lentgh = parseInt("${s.substring(0, firstColon)}") = ${current_lentgh}`
        );

        let i = 0;
        let iteration = 0;

        while (i < s.length) {
            iteration++;
            console.log(`\n--- itération ${iteration} ---`);
            console.log(`  ENTRÉE : i=${i}, current_index=${current_index}, current_lentgh=${current_lentgh}, last_index=${last_index}`);

            if (iteration > MAX_ITERATIONS) {
                console.log(`  ⚠️  MAX_ITERATIONS (${MAX_ITERATIONS}) dépassé — boucle infinie détectée, arrêt forcé.`);
                console.log(`  i vaut ${i} et ne progresse plus vers s.length (${s.length}).`);
                break;
            }

            last_index = current_index + current_lentgh ;    
            console.log(`  last_index = current_index(${current_index}) + current_lentgh(${current_lentgh}) = ${last_index}`);

            const srt = s.substring(current_index + 1, last_index + 1);
            console.log(`  srt = s.substring(${current_index + 1}, ${last_index}) = "${srt}"`);

            current_index = s.indexOf(":", last_index);
            console.log(`  current_index = s.indexOf(":", ${last_index}) = ${current_index}`);

            let lengthSlice = s.substring(last_index + 1, current_index);
            current_lentgh = parseInt(lengthSlice);
            console.log(`  current_lentgh = parseInt(s.substring(${last_index + 1}, ${current_index})="${lengthSlice}") = ${current_lentgh}`);

            decodedStrings.push(srt);
            console.log(`  push("${srt}") → decodedStrings = ${JSON.stringify(decodedStrings)}`);

            const newI = last_index + 1;
            console.log(`  i = last_index(${last_index}) + current_index(${current_index}) = ${newI}`);
            i = newI;

            if (Number.isNaN(current_index) || Number.isNaN(current_lentgh) || Number.isNaN(i)) {
                console.log(`  ⚠️  NaN détecté dans une variable de contrôle — la boucle va se comporter de façon imprévisible.`);
            }
        }

        console.log(`\nRÉSULTAT FINAL : ${JSON.stringify(decodedStrings)}`);
        return decodedStrings;
    }
    // --- Static method (belongs to the class, not an instance) ---
    static create(delimiter?: string): Codec {
        return new Codec(delimiter);
    }

    // --- Getter/setter (optional) ---
    get separator(): string {
        return this.delimiter;
    }
}

// --- encode() : reprise telle quelle, elle ne semble pas buguée -------------

export function encode(strs: string[]): string {
    let encodedString: string = "";
    for (const s of strs) {
        if (s.includes(':')) {
            throw new Error("Input strings cannot contain the delimiter ':'");
        } else if (s.includes('#')) {
            throw new Error("Input strings cannot contain the delimiter '#'");
        } else if (s.length > 1000) {
            throw new Error("Input strings cannot exceed 1000 characters in length");
        } else if (s.length === 0) {
            throw new Error("Input strings cannot be empty");
        } else if (s.length < 1) {
            throw new Error("Input strings must have at least 1 character");
        } else {
            encodedString += `${s.length}:${s}`;
        }
    }
    return encodedString;
}

// --- Version 1 : Codec.decode() instrumentée (logique inchangée) -----------

export function decode(s: string): string[] {
    separator(`Codec.decode("${s}")`);

    let decodedStrings: string[] = [];
    let current_index = 0;
    let current_lentgh = 0;
    let last_index = 0;

    const firstColon = s.indexOf(":", 0);
    current_index = s.indexOf(":", 0);
    current_lentgh = parseInt(s.substring(0, firstColon));
    console.log(
        `[init] firstColon=${firstColon}, ` +
        `current_lentgh = parseInt("${s.substring(0, firstColon)}") = ${current_lentgh}`
    );

    let i = 0;
    let iteration = 0;

    while (i < s.length) {
        iteration++;
        console.log(`\n--- itération ${iteration} ---`);
        console.log(`  ENTRÉE : i=${i}, current_index=${current_index}, current_lentgh=${current_lentgh}, last_index=${last_index}`);

        if (iteration > MAX_ITERATIONS) {
            console.log(`  ⚠️  MAX_ITERATIONS (${MAX_ITERATIONS}) dépassé — boucle infinie détectée, arrêt forcé.`);
            console.log(`  i vaut ${i} et ne progresse plus vers s.length (${s.length}).`);
            break;
        }

        last_index = current_index + current_lentgh ;    
        console.log(`  last_index = current_index(${current_index}) + current_lentgh(${current_lentgh}) = ${last_index}`);

        const srt = s.substring(current_index + 1, last_index + 1);
        console.log(`  srt = s.substring(${current_index + 1}, ${last_index}) = "${srt}"`);

        current_index = s.indexOf(":", last_index);
        console.log(`  current_index = s.indexOf(":", ${last_index}) = ${current_index}`);

        let lengthSlice = s.substring(last_index + 1, current_index);
        current_lentgh = parseInt(lengthSlice);
        console.log(`  current_lentgh = parseInt(s.substring(${last_index + 1}, ${current_index})="${lengthSlice}") = ${current_lentgh}`);

        decodedStrings.push(srt);
        console.log(`  push("${srt}") → decodedStrings = ${JSON.stringify(decodedStrings)}`);

        const newI = last_index + 1;
        console.log(`  i = last_index(${last_index}) + current_index(${current_index}) = ${newI}`);
        i = newI;

        if (Number.isNaN(current_index) || Number.isNaN(current_lentgh) || Number.isNaN(i)) {
            console.log(`  ⚠️  NaN détecté dans une variable de contrôle — la boucle va se comporter de façon imprévisible.`);
        }
    }

    console.log(`\nRÉSULTAT FINAL : ${JSON.stringify(decodedStrings)}`);
    return decodedStrings;
}

// --- Version 2 : decode() standalone instrumentée (logique inchangée) ------

function debugStandaloneDecode(s: string): string[] {
    separator(`decode("${s}") — version split(':')`);

    let decodedStrings: string[] = [];
    let i = 0;

    const parts = s.split(':');
    console.log(`s.split(':') = ${JSON.stringify(parts)}`);
    console.log(`(nombre de fragments : ${parts.length})`);

    let iteration = 0;
    for (const str of parts) {
        iteration++;
        console.log(`\n--- fragment ${iteration}: "${str}" ---`);

        if (str.length === 0) {
            console.log(`  ⚠️  throw: "Decoded string cannot be empty" (fragment vide)`);
            throw new Error("Decoded string cannot be empty");
        }

        if (str.includes(':')) {
            console.log(`  contient ':' → continue (mais split() a déjà retiré tous les ':', ce cas n'arrive jamais)`);
            continue;
        } else {
            decodedStrings[i] = str;
            console.log(`  decodedStrings[${i}] = "${str}" → ${JSON.stringify(decodedStrings)}`);
            i++;
        }
    }

    console.log(`\nRÉSULTAT FINAL : ${JSON.stringify(decodedStrings)}`);
    return decodedStrings;
}

// --- Exécution -----------------------------------------------------------------
// 
// function main(): void {
//     const input = ['Hello', 'World', "World"];
//     console.log(`INPUT : ${JSON.stringify(input)}`);
// 
//     const encoded = encode(input);
//     console.log(`encode(input) = "${encoded}"`);
// 
//     let resultCodec: string[] = [];
//     try {
//         resultCodec = debugCodecDecode(encoded);
//     } catch (err) {
//         console.log(`\n❌ Codec.decode a levé une exception : ${(err as Error).message}`);
//     }
// 
//     // let resultStandalone: string[] = [];
//     // try {
//     //     resultStandalone = debugStandaloneDecode(encoded);
//     // } catch (err) {
//     //     console.log(`\n❌ decode standalone a levé une exception : ${(err as Error).message}`);
//     // }
// 
//     separator('COMPARAISON AVEC L\'ATTENDU');
//     console.log(`Attendu           : ${JSON.stringify(input)}`);
//     console.log(`Codec.decode      : ${JSON.stringify(resultCodec)}  ${JSON.stringify(resultCodec) === JSON.stringify(input) ? '✓' : '✗'}`);
//     console.log(`decode standalone : ${JSON.stringify(resultStandalone)}  ${JSON.stringify(resultStandalone) === JSON.stringify(input) ? '✓' : '✗'}`);
// }
// 
// main();
// 