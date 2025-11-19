import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const day = searchParams.get('day') ?? '0';  

  const backendUrl = `${process.env.NEXT_PUBLIC_API_URL}/gen-predictions/?day=${day}`;

  try {
    const res = await fetch(backendUrl, {
      cache: 'no-store',
      headers: { 'Accept': 'application/json' },
    });

    if (!res.ok) {
      const text = await res.text();
      console.error('Backend error:', res.status, text);
      return NextResponse.json(
        { error: `Backend returned ${res.status}` },
        { status: 502 }
      );
    }

    const data = await res.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Proxy failed:', error.message);
    return NextResponse.json(
      { error: 'Backend unreachable', details: error.message },
      { status: 500 }
    );
  }
}