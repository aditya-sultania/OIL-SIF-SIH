from main import classify_text

CASES = {
    'guy fell from 10th floor': 'critical',
    'a guy drilled his hand': 'high',
    'someone smelled something burning': 'high',
    'someone smelled smoke': 'high',
    'worker smelled gas': 'high',
    'worker got electric shock': 'critical',
    'worker bypassed lockout': 'high',
    'worker caught his hand in a machine': 'critical',
    'worker entered confined space without permit': 'high',
    'small water spill on floor': 'model',
}

if __name__ == '__main__':
    failed = []
    for text, expected in CASES.items():
        result = classify_text(text)
        actual = result['evidence_level']
        print(f'{text!r} -> {actual} / {result["sif_probability"]}% / {result["evidence_reason"]}')
        if actual != expected:
            failed.append((text, expected, actual))
    if failed:
        raise SystemExit(f'FAILED: {failed}')
    print('All safety-screening regression tests passed.')
